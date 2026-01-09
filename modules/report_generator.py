import json
from datetime import datetime
from typing import Dict, List
import os

class ReportGenerator:
    def __init__(self, output_dir: str = 'reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_html_report(self, drift_data: Dict) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.output_dir}/drift_report_{timestamp}.html"
        
        html_content = self._create_html(drift_data)
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        # Also create/update index.html as latest
        with open(f"{self.output_dir}/index.html", 'w') as f:
            f.write(html_content)
        
        return filename
    
    def _create_html(self, data: Dict) -> str:
        drifts = data.get('drifts', [])
        summary = data.get('summary', {})
        
        severity_colors = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745'
        }
        
        drift_rows = ""
        for drift in drifts:
            severity = drift.get('severity', 'low')
            color = severity_colors.get(severity, '#6c757d')
            
            drift_rows += f"""
            <tr>
                <td><span class="badge" style="background-color: {color}">{severity.upper()}</span></td>
                <td><code>{drift.get('resource_address', 'N/A')}</code></td>
                <td>{drift.get('resource_type', 'N/A')}</td>
                <td>{drift.get('change_type', 'N/A')}</td>
                <td>{drift.get('details', 'N/A')}</td>
            </tr>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terraform Drift Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #f5f5f5; color: #333; }}
        .container {{ max-width: 1200px; margin: 20px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 15px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #e9ecef; }}
        .summary-card h3 {{ margin: 0; font-size: 2.5em; color: #2c3e50; }}
        .summary-card p {{ margin: 10px 0 0 0; color: #6c757d; font-weight: 500; }}
        .chart-container {{ position: relative; height: 300px; width: 100%; margin: 40px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #e9ecef; }}
        th {{ background-color: #343a40; color: white; font-weight: 600; text-transform: uppercase; font-size: 0.85em; }}
        tr:hover {{ background-color: #f8f9fa; }}
        .badge {{ padding: 6px 12px; border-radius: 20px; color: white; font-size: 0.85em; font-weight: bold; display: inline-block; }}
        code {{ background: #f1f3f5; padding: 4px 8px; border-radius: 4px; font-family: 'Consolas', monospace; color: #e83e8c; }}
        .footer {{ margin-top: 40px; text-align: center; color: #adb5bd; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Terraform Drift Detection Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Environment: <strong>{summary.get('environment', 'Unknown').upper()}</strong></p>
        
        <div class="summary">
            <div class="summary-card">
                <h3>{summary.get('total_resources', 0)}</h3>
                <p>Total Resources</p>
            </div>
            <div class="summary-card">
                <h3 style="color: {severity_colors['critical']}">{summary.get('critical_count', 0)}</h3>
                <p>Critical Issues</p>
            </div>
            <div class="summary-card">
                <h3 style="color: {severity_colors['high']}">{summary.get('high_count', 0)}</h3>
                <p>High Severity</p>
            </div>
             <div class="summary-card">
                <h3>{summary.get('drift_percentage', 0):.1f}%</h3>
                <p>Drift Percentage</p>
            </div>
        </div>

        <div class="chart-container">
            <canvas id="driftChart"></canvas>
        </div>
        
        <h2>Detected Drift Details</h2>
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Resource Address</th>
                    <th>Type</th>
                    <th>Change</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {drift_rows if drift_rows else '<tr><td colspan="5" style="text-align:center; padding: 30px;">✅ No drift detected. Infrastructure is in sync.</td></tr>'}
            </tbody>
        </table>

        <div class="footer">
            <p>Generated by Enhanced Terraform Drift Detector</p>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('driftChart').getContext('2d');
        const driftChart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['Critical', 'High', 'Medium', 'Low', 'In Sync'],
                datasets: [{{
                    data: [
                        {summary.get('critical_count', 0)},
                        {summary.get('high_count', 0)},
                        {summary.get('medium_count', 0)},
                        {summary.get('low_count', 0)},
                        {max(0, summary.get('total_resources', 0) - summary.get('drifted_resources', 0))}
                    ],
                    backgroundColor: [
                        '{severity_colors['critical']}',
                        '{severity_colors['high']}',
                        '{severity_colors['medium']}',
                        '{severity_colors['low']}',
                        '#e9ecef'
                    ],
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom' }},
                    title: {{ display: true, text: 'Resource Status Distribution' }}
                }}
            }}
        }});
    </script>
</body>
</html>
        """
        
        return html
