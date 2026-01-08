#!/usr/bin/env python3

import yaml
import sys
from pathlib import Path
from terraform_client import TerraformClient
from drift_analyzer import DriftAnalyzer
from reporters.console_reporter import ConsoleReporter
from reporters.json_reporter import JSONReporter


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def detect_drift_for_environment(env_config: dict, config: dict, project_root: Path) -> dict:
    """Run drift detection for a single environment"""
    
    env_name = env_config['name']
    # Resolve environment path relative to the project root for robustness
    env_path = project_root / env_config['path']
    if not env_path.is_dir():
        print(f"   ❌ Environment path does not exist: {env_path}")
        return None
    
    print(f"\n🔍 Checking drift for environment: {env_name}")
    print(f"   Path: {env_path}")
    
    # Initialize Terraform client
    tf_client = TerraformClient(env_path)
    
    # Initialize Terraform (in case it hasn't been)
    print("   Initializing Terraform...")
    success, output = tf_client.init()
    if not success:
        print(f"   ❌ Failed to initialize Terraform: {output}")
        return None
    
    # Run terraform plan with detailed exit code
    print("   Running terraform plan...")
    exit_code, stdout, stderr = tf_client.plan(detailed_exitcode=True)
    
    if exit_code == 1:
        print(f"   ❌ Terraform plan failed: {stderr}")
        return None
    
    # Analyze drift
    analyzer = DriftAnalyzer(config)
    drift_report = analyzer.analyze_drift(env_name, stdout, exit_code)
    
    return drift_report


def main():
    
    print("="*80)
    print("🚀 Infrastructure Drift Detector")
    print("="*80)

    # Define project root relative to this script's location
    project_root = Path(__file__).parent.parent.resolve()
    
    # Load configuration
    try:
        config = load_config()
    except FileNotFoundError:
        print("❌ config.yaml not found!")
        sys.exit(1)
    
    # Get enabled environments
    environments = [
        env for env in config['terraform']['environments']
        if env.get('enabled', True)
    ]
    
    if not environments:
        print("⚠️  No enabled environments found in config.yaml")
        sys.exit(0)
    
    # Initialize reporters
    reporters = []
    if 'console' in config['reporting']['formats']:
        reporters.append(ConsoleReporter())
    if 'json' in config['reporting']['formats']:
        reporters.append(JSONReporter(config['reporting']['output_dir']))
    
    # Check drift for each environment
    all_reports = []
    for env_config in environments:
        drift_report = detect_drift_for_environment(env_config, config, project_root)
        
        if drift_report:
            all_reports.append(drift_report)
            
            # Report using all configured reporters
            for reporter in reporters:
                reporter.report(drift_report)
    
    # Summary
    print("\n" + "="*80)
    print("📊 DRIFT DETECTION SUMMARY")
    print("="*80)
    
    drift_count = sum(1 for r in all_reports if r['drift_detected'])
    
    if drift_count > 0:
        print(f"⚠️  Drift detected in {drift_count}/{len(all_reports)} environment(s)")
        sys.exit(1)  # Exit with error code if drift found
    else:
        print(f"✅ No drift detected in any environment")
        sys.exit(0)


if __name__ == "__main__":
    main()