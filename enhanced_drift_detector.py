import os
import yaml
import argparse
import sys
from datetime import datetime
from dotenv import load_dotenv

# Ensure modules can be imported
sys.path.append(os.getcwd())

from modules.severity_scorer import SeverityScorer
from modules.history_tracker import HistoryTracker
from modules.notifications import NotificationService
from modules.report_generator import ReportGenerator
from modules.terraform_client import TerraformClient
from modules.drift_analyzer import DriftAnalyzer
from modules.dependency_mapper import DependencyMapper

# Load environment variables
load_dotenv('config/.env')

def main():
    parser = argparse.ArgumentParser(description='Enhanced Terraform Drift Detector')
    parser.add_argument('--environment', default='production', help='Environment to scan')
    parser.add_argument('--terraform-dir', default='.', help='Terraform directory')
    parser.add_argument('--no-notify', action='store_true', help='Skip notifications')
    args = parser.parse_args()
    
    # Load configuration
    try:
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/config.yaml not found. Please ensure the configuration file exists.")
        return 1
    
    
    # Override notification config with environment variables
    notification_config = config['notifications'].copy()
    notification_config['slack_webhook'] = os.getenv('SLACK_WEBHOOK_URL', '')
    notification_config['sns_topic_arn'] = os.getenv('SNS_TOPIC_ARN', '')
    
    try:
        scorer = SeverityScorer()
        tracker = HistoryTracker(config['history']['dynamodb_table'])
        notifier = NotificationService(notification_config)
        reporter = ReportGenerator(config['reporting']['output_dir'])
        mapper = DependencyMapper(args.terraform_dir)
    except Exception as e:
        print(f"Error initializing modules: {e}")
        return 1
    
    print(f"🔍 Starting drift detection for {args.environment}...")
    
    # Run drift detection
    drift_results = detect_drift(args.terraform_dir, config, args.environment)
    
    # Generate Dependency Graph
    graph_path = mapper.generate_graph(config['reporting']['output_dir'])

    # Enhance with severity scoring
    enhanced_drifts = []
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    
    for drift in drift_results:
        score = scorer.score_change(
            drift['resource_type'],
            drift['change_type'],
            drift.get('attribute', '')
        )
        
        drift['severity'] = score['severity']
        drift['score'] = score['score']
        enhanced_drifts.append(drift)
        severity_counts[score['severity']] += 1
    
    # Sort by severity score
    enhanced_drifts.sort(key=lambda x: x['score'], reverse=True)
    
    # Prepare summary
    summary = {
        'environment': args.environment,
        'timestamp': datetime.now().isoformat(),
        'total_resources': len(drift_results),  # Approximation
        'drifted_resources': len(enhanced_drifts),
        'drift_percentage': (len(enhanced_drifts) / max(len(drift_results), 1)) * 100 if drift_results else 0,
        'critical_count': severity_counts['critical'],
        'high_count': severity_counts['high'],
        'medium_count': severity_counts['medium'],
        'low_count': severity_counts['low'],
        'dependency_graph': graph_path
    }
    
    # Generate report
    report_path = reporter.generate_html_report({
        'drifts': enhanced_drifts,
        'summary': summary
    })
    print(f"📄 Report generated: {report_path}")
    
    # Save to history
    if config['history']['enabled']:
        scan_id = tracker.save_scan_result({
            **summary,
            'drift_details': enhanced_drifts
        })
        print(f"💾 Scan saved to history: {scan_id}")
    
    # Send notifications
    if not args.no_notify and enhanced_drifts:
        notifier.notify_drift({
            **summary,
            'highest_severity': enhanced_drifts[0]['severity'] if enhanced_drifts else 'none',
            'report_url': f"file://{os.path.abspath(report_path)}"
        })
        print("📧 Notifications sent")
    
    print(f"\n✅ Scan complete: {len(enhanced_drifts)} drifts detected")
    return 0 if not enhanced_drifts else 1

def detect_drift(terraform_dir, config, environment):
    """
    Detects drift in the given Terraform directory.
    Returns a list of flattened drift dictionaries.
    """
    
    # Initialize Core Drift Detection Componenets
    try:
        tf_client = TerraformClient(terraform_dir)
        
        # Run Init (optional, but good practice)
        print("Running terraform init...")
        success, msg = tf_client.init()
        if not success:
            print(f"Warning: Terraform init failed or had output: {msg}")

        # Run Plan
        print("Running terraform plan...")
        exit_code, stdout, stderr = tf_client.plan()
        
        if exit_code == 1:
            print(f"Terraform plan failed: {stderr}")
            return []
        
        if exit_code == 0:
            print("No drift detected by Terraform.")
            return []

    except Exception as e:
        print(f"Error executing Terraform: {e}")
        return []

    # Analyze Plan
    analyzer = DriftAnalyzer(config)
    analysis_result = analyzer.analyze_drift(environment, stdout, exit_code)
    filtered_drift = analysis_result.get('filtered_drift', {})

    flat_drifts = []

    # Process Changed Resources
    for res in filtered_drift.get('resources_to_change', []):
        address = res.get('address')
        rtype = res.get('type')
        is_replacement = res.get('is_replacement', False)
        
        # If there are specific attribute changes
        if res.get('changes'):
            for change in res.get('changes'):
                flat_drifts.append({
                    'resource_address': address,
                    'resource_type': rtype,
                    'change_type': 'replace' if is_replacement else 'update',
                    'attribute': change.get('attribute'),
                    'details': change.get('change')
                })
        else:
            # Fallback if no specific changes listed (e.g. just a general change)
            flat_drifts.append({
                'resource_address': address,
                'resource_type': rtype,
                'change_type': 'replace' if is_replacement else 'update',
                'attribute': 'general',
                'details': 'Resource changed'
            })

    # Process Destroyed Resources
    for res in filtered_drift.get('resources_to_destroy', []):
        address = res.get('address')
        # Infer type from address if possible
        rtype = 'unknown'
        if '.' in address:
            parts = address.split('.')
            if len(parts) >= 2:
                rtype = parts[-2]
                
        flat_drifts.append({
            'resource_address': address,
            'resource_type': rtype,
            'change_type': 'destroy',
            'attribute': 'all',
            'details': 'Resource will be destroyed'
        })

    # Process Added Resources (Usually not considered 'drift' in the negative sense, but nice to track)
    # The original enhance script logic focuses on drift as something to fix (severity).
    # Adding resources might be "info". 
    for res in filtered_drift.get('resources_to_add', []):
        address = res.get('address')
        rtype = 'unknown'
        if '.' in address:
             parts = address.split('.')
             if len(parts) >= 2:
                 rtype = parts[-2]
        
        flat_drifts.append({
            'resource_address': address,
            'resource_type': rtype,
            'change_type': 'create',
            'attribute': 'all',
            'details': 'Resource will be created'
        })

    return flat_drifts

if __name__ == '__main__':
    exit(main())
