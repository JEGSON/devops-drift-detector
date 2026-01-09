import boto3
import requests
import json
from datetime import datetime
from typing import Dict, List

class NotificationService:
    def __init__(self, config: Dict):
        self.config = config
        self.sns_client = boto3.client('sns')
    
    
    def send_slack(self, summary: Dict, severity: str):
        webhook_url = self.config.get('slack_webhook')
        if not webhook_url:
            return
        
        colors = {
            'critical': '#FF0000',
            'high': '#FF6600',
            'medium': '#FFCC00',
            'low': '#00FF00',
            'none': '#36a64f'  # Green for success
        }
        
        color = colors.get(severity, '#808080')
        title = f"Terraform Drift Report: {summary.get('environment', 'Unknown').upper()}"
        
        # Build Fields
        fields = [
            {'title': 'Total Resources', 'value': str(summary.get('total_resources', 0)), 'short': True},
            {'title': 'Drifted Resources', 'value': str(summary.get('drifted_resources', 0)), 'short': True},
            {'title': 'Critical Issues', 'value': str(summary.get('critical_count', 0)), 'short': True},
            {'title': 'High Severity Issues', 'value': str(summary.get('high_count', 0)), 'short': True}
        ]
        
        # Build Top 5 Drifts
        top_drifts_text = ""
        drifts = summary.get('drift_details', [])
        if drifts:
            top_5 = sorted(drifts, key=lambda x: x.get('score', 0), reverse=True)[:5]
            for d in top_5:
                # Add emoji based on change type
                icon = "🔥" if d.get('severity') == 'critical' else "⚠️"
                change = "DESTROY" if d.get('change_type') == 'destroy' else "MODIFY"
                top_drifts_text += f"{icon} *{d.get('resource_address')}* ({change})\n"
        else:
            top_drifts_text = "✅ No drift detected. Infrastructure is in sync."
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{title}*\nSeverity: *{severity.upper()}*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*{f['title']}*:\n{f['value']}"} for f in fields
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Top Drifts (Priority)*:\n" + top_drifts_text
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"View full report: {summary.get('report_url', 'N/A')}"
                    }
                ]
            }
        ]

        # Payload structure depends on whether you use blocks (modern) or attachments (legacy)
        # Using blocks for better formatting
        payload = {
            "blocks": blocks,
            "attachments": [
                {
                    "color": color,
                    "blocks": []  # purely for the color bar
                }
            ]
        }
        
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send Slack notification: {e}")

    def send_sns(self, subject: str, message: str):
        topic_arn = self.config.get('sns_topic_arn')
        if not topic_arn:
            return
        
        try:
            self.sns_client.publish(
                TopicArn=topic_arn,
                Subject=subject,
                Message=message
            )
        except Exception as e:
            print(f"Failed to send SNS notification: {e}")
    
    def notify_drift(self, drift_summary: Dict):
        severity = drift_summary.get('highest_severity', 'none')
        alert_levels = self.config.get('alert_on_severity', ['critical', 'high', 'medium', 'low'])
        
        # Always notify if drift implies severity OR if configured to notify on success (optional)
        # For now, we follow the config. If 'none' (success) is not in alert_levels, we skip.
        # But typically users want a periodic "All Good" message or at least know the scan ran.
        # Let's assume if 'low' is enabled, 'none' might not be. 
        # But the user asked for "Success messages when no drift found".
        # So we force send if drift count is 0, or check specific config.
        
        if severity == 'none' and drift_summary.get('drifted_resources', 0) == 0:
             # Success case
             pass # proceed to send
        elif severity not in alert_levels:
            return
        
        # Slack (Rich)
        self.send_slack(drift_summary, severity)
        
        # SNS (Text only) - Only for actual issues usually, or critical/high
        if severity in ['critical', 'high']:
            message = self._format_message(drift_summary)
            self.send_sns(f"Terraform Drift - {severity.upper()}", message)
    
    def _format_message(self, summary: Dict) -> str:
        return f"""
Drift Detection Summary:
- Environment: {summary.get('environment', 'N/A')}
- Drifted Resources: {summary.get('drifted_resources', 0)}
- Highest Severity: {summary.get('highest_severity', 'N/A')}
- Critical Issues: {summary.get('critical_count', 0)}
- High Issues: {summary.get('high_count', 0)}

View detailed report: {summary.get('report_url', 'N/A')}
        """.strip()
