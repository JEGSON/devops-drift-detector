# Enhanced Terraform Drift Detector

> **Enterprise-grade Infrastructure Drift Detection and Monitoring System**

A comprehensive, production-ready Terraform drift detection platform featuring advanced severity scoring, intelligent alerting, visual reporting, automated remediation suggestions, and complete CI/CD integration.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=flat&logo=terraform&logoColor=white)](https://www.terraform.io/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Notifications](#-notifications)
- [Reporting](#-reporting)
- [Troubleshooting](#-troubleshooting)
- [Advanced Topics](#-advanced-topics)
- [Contributing](#-contributing)

---

## 🎯 Overview

**Configuration drift** occurs when infrastructure resources are manually modified outside of Infrastructure-as-Code workflows, causing operational inconsistencies and security vulnerabilities. This tool provides:

- **🔍 Intelligent Drift Detection** - Automated scanning with configurable schedules
- **📊 Visual Reporting** - Interactive HTML dashboards with Chart.js visualizations
- **🚨 Multi-Channel Alerting** - Slack, SNS, and email notifications
- **📈 Historical Tracking** - DynamoDB-backed drift history and trend analysis
- **🔧 Actionable Remediation** - Specific Terraform commands to fix detected drift
- **🌐 Dependency Mapping** - Resource relationship visualization
- **⚙️ Smart Filtering** - Policy-based drift categorization
- **🔒 Security-Focused** - Severity scoring emphasizing security-critical resources

---

## ✨ Features

### 🎯 Core Detection Engine

| Feature | Description | Status |
|---------|-------------|--------|
| **Severity Scoring System** | Classifies drift as Critical, High, Medium, or Low based on resource type and attributes | ✅ Implemented |
| **DynamoDB History Tracking** | Stores drift scan results with timestamps for trend analysis | ✅ Implemented |
| **Smart Policy Filtering** | Configurable rules to ignore expected drift and highlight critical changes | ✅ Implemented |
| **Resource Dependency Mapping** | Generates Terraform graph visualizations showing resource relationships | ✅ Implemented |

### 📢 Alerting & Notifications

| Channel | Features | Status |
|---------|----------|--------|
| **Slack Integration** | Rich messages with color-coding, drift summaries, top 5 resources, success alerts | ✅ Implemented |
| **AWS SNS** | Email/SMS notifications for critical and high-severity drift | ✅ Implemented |
| **GitHub Issues** | Automatic issue creation with detailed drift reports | ✅ Implemented |

### 📊 Reporting & Visualization

| Report Type | Description | Status |
|-------------|-------------|--------|
| **HTML Dashboard** | Interactive reports with Chart.js doughnut charts, severity breakdowns | ✅ Implemented |
| **JSON Export** | Machine-readable drift data for integration with other tools | ✅ Implemented |
| **Dependency Graphs** | DOT format graphs for Graphviz visualization | ✅ Implemented |

### 🤖 Automation & CI/CD

| Feature | Description | Status |
|---------|-------------|--------|
| **Cron-based Scheduling** | Automated drift scans every 6 hours via crontab | ✅ Implemented |
| **GitHub Actions Workflow** | CI/CD pipeline for automated scanning and deployment | ✅ Implemented |
| **Terraform Plan Integration** | Seamless integration with terraform init/plan/apply workflows | ✅ Implemented |

### 🔧 Remediation & Insights

| Feature | Description | Status |
|---------|-------------|--------|
| **Actionable Commands** | Specific `terraform apply -target=` suggestions for each drifted resource | ✅ Implemented |
| **Severity-based Prioritization** | Focus on critical security and networking changes first | ✅ Implemented |
| **Policy Engine** | Define ignored resources, critical resources, and allowed drift patterns | ✅ Implemented |

---

## 🏗️ Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    Enhanced Drift Detector                        │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Core Detection Engine                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │  Terraform   │→ │    Drift     │→ │   Severity   │    │ │
│  │  │   Client     │  │   Analyzer   │  │    Scorer    │    │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │ │
│  │         ↓                  ↓                  ↓           │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │           Policy Engine (Filtering)               │    │ │
│  │  └────────────────────┬─────────────────────────────┘    │ │
│  └───────────────────────┼──────────────────────────────────┘ │
│                          ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                Output & Alerting                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│ │
│  │  │   HTML   │  │  Slack   │  │   SNS    │  │ History  ││ │
│  │  │  Report  │  │  Alert   │  │  Email   │  │(DynamoDB)││ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘│ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### Module Structure

```
enhanced_drift_detector.py (Main Orchestrator)
    ↓
    ├─→ modules/terraform_client.py      (Terraform operations)
    ├─→ modules/drift_analyzer.py        (Drift detection logic)
    ├─→ modules/policy_engine.py         (Smart filtering)
    ├─→ modules/severity_scorer.py       (Severity classification)
    ├─→ modules/history_tracker.py       (DynamoDB persistence)
    ├─→ modules/notifications.py         (Slack/SNS/Email)
    ├─→ modules/report_generator.py      (HTML/JSON reports)
    └─→ modules/dependency_mapper.py     (Resource graphs)
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/JEGSON/devops-drift-detector.git
cd devops-drift-detector

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r drift-detector/requirements.txt
```

### 2. Configure AWS

```bash
# Configure AWS credentials
aws configure

# Create S3 bucket for Terraform state
BUCKET_NAME="terraform-state-drift-detector-$(date +%s)"
aws s3 mb s3://${BUCKET_NAME} --region us-east-1
aws s3api put-bucket-versioning --bucket ${BUCKET_NAME} --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket ${BUCKET_NAME} \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

# Save bucket name
echo "TERRAFORM_STATE_BUCKET=${BUCKET_NAME}" >> config/.env
```

### 3. Update Configuration

Edit `terraform/environments/dev/main.tf` and `config/.env`:

```hcl
# terraform/environments/dev/main.tf
backend "s3" {
  bucket = "YOUR_BUCKET_NAME_FROM_STEP_2"
  key    = "dev/terraform.tfstate"
  region = "us-east-1"
}
```

```bash
# config/.env
AWS_REGION=us-east-1
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789:terraform-drift-alerts
DYNAMODB_TABLE=terraform-drift-history
```

### 4. Deploy Infrastructure

```bash
cd terraform/environments/dev
terraform init
terraform apply
```

### 5. Run Drift Detector

```bash
cd ../../../
python enhanced_drift_detector.py --environment dev --terraform-dir ./terraform/environments/dev
```

**Expected Output:**
```
🔍 Starting drift detection for dev...
Running terraform init...
Running terraform plan...
No drift detected by Terraform.
🕸️  Generating dependency graph...
📄 Report generated: reports/drift_report_20260109_203307.html
💾 Scan saved to history: scan_1767987187
📧 Notifications sent

✅ Scan complete: 0 drifts detected
```

---

## 📦 Prerequisites

### Required Tools

- **Python** 3.11 or higher
- **Terraform** 1.0 or higher
- **AWS CLI** configured with credentials
- **Git** for version control

### AWS Services Used

| Service | Purpose | Cost |
|---------|---------|------|
| **S3** | Terraform state storage | ~$0.01/month (Free Tier eligible) |
| **DynamoDB** | State locking + drift history | Free Tier eligible |
| **SNS** | Email/SMS notifications | ~$0.50/1000 emails |
| **EC2** | Example infrastructure | Free Tier eligible (t3.micro) |

### Python Dependencies

```
boto3>=1.28.0           # AWS SDK
python-terraform>=0.10.1 # Terraform wrapper
pyyaml>=6.0             # YAML config parsing
colorama>=0.4.6         # Terminal colors
tabulate>=0.9.0         # Table formatting
python-dotenv>=1.0.0    # Environment variables
requests>=2.31.0        # HTTP client (Slack)
```

---

## 🔧 Installation

### Option 1: Standard Installation

```bash
# Clone repository
git clone https://github.com/JEGSON/devops-drift-detector.git
cd devops-drift-detector

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r drift-detector/requirements.txt

# Copy example configs
cp config/.env.example config/.env
# Edit config/.env with your values
```

### Option 2: Docker (Coming Soon)

```bash
docker pull jegson/drift-detector:latest
docker run -v $(pwd)/config:/app/config drift-detector
```

---

## ⚙️ Configuration

### Main Configuration (`config/config.yaml`)

```yaml
aws:
  region: us-east-1
  profile: default

scanning:
  schedule: "0 */6 * * *"  # Every 6 hours
  parallel_checks: 5
  timeout: 300

severity:  # Now loaded from config/severity_rules.yaml
  critical:
    - aws_security_group
    - aws_iam_role
    - aws_iam_policy
  high:
    - aws_db_instance
    - aws_s3_bucket
  medium:
    - aws_instance
    - aws_lambda_function
  low:
    - aws_s3_bucket_object

notifications:
  slack_webhook: "${SLACK_WEBHOOK_URL}"
  sns_topic_arn: "${SNS_TOPIC_ARN}"
  alert_on_severity:
    - critical
    - high

reporting:
  format: html
  output_dir: reports
  retention_days: 90

history:
  dynamodb_table: terraform-drift-history
  enabled: true
```

### Severity Rules (`config/severity_rules.yaml`)

Customize resource severity classifications:

```yaml
severity:
  critical:
    - aws_iam_role
    - aws_iam_policy
    - aws_security_group
    - aws_vpc
    - aws_kms_key
  
  high:
    - aws_db_instance
    - aws_rds_cluster
    - aws_s3_bucket
    - aws_eks_cluster
  
  medium:
    - aws_instance
    - aws_lambda_function
    - aws_dynamodb_table
  
  low:
    - aws_cloudwatch_log_group
    - aws_s3_bucket_object
```

### Environment Variables (`config/.env`)

```bash
# AWS Configuration
AWS_PROFILE=default
AWS_REGION=us-east-1

# Slack Integration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# SNS Configuration
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789:terraform-drift-alerts

# DynamoDB
DYNAMODB_TABLE=terraform-drift-history

# Terraform State
TERRAFORM_STATE_BUCKET=terraform-state-drift-detector-1234567890
```

---

## 💻 Usage

### Manual Drift Detection

```bash
# Activate virtual environment
source .venv/bin/activate

# Run for specific environment
python enhanced_drift_detector.py --environment dev --terraform-dir ./terraform/environments/dev

# Skip notifications (testing)
python enhanced_drift_detector.py --environment dev --terraform-dir ./terraform/environments/dev --no-notify
```

### Automated Scheduling (Cron)

The project includes a wrapper script for cron automation:

```bash
# View cron job
crontab -l

# Expected output:
# 0 */6 * * * /Users/wealth/devops-drift-detector/scripts/run_drift_scan.sh

# Check logs
tail -f logs/cron.log
```

### Creating Drift for Testing

1. **Apply infrastructure first:**
   ```bash
   cd terraform/environments/dev
   terraform apply
   ```

2. **Cause drift manually:**
   - Go to AWS Console → EC2 → Instances
   - Select your instance
   - Add/modify a tag: `Manual=test`

3. **Run detector:**
   ```bash
   cd ../../..
   python enhanced_drift_detector.py --environment dev --terraform-dir ./terraform/environments/dev
   ```

4. **Check Slack for alert** with detected drift details!

5. **Fix drift:**
   ```bash
   cd terraform/environments/dev
   terraform apply  # Removes manual changes
   ```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow (`.github/workflows/drift_scan.yml`)

```yaml
name: Terraform Drift Detection

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:       # Manual trigger

jobs:
  drift_scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install Terraform
        uses: hashicorp/setup-terraform@v3
      
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      
      - name: Run Drift Detector
        run: |
          python enhanced_drift_detector.py \
            --environment production \
            --terraform-dir ./terraform/environments/prod
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: drift-report
          path: reports/*.html
```

### Required GitHub Secrets

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ROLE_ARN` | IAM role for OIDC authentication | `arn:aws:iam::123456789:role/GithubActions` |
| `AWS_ACCESS_KEY_ID` | Alternative to OIDC | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Alternative to OIDC | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook | `https://hooks.slack.com/services/...` |
| `SNS_TOPIC_ARN` | SNS topic for alerts | `arn:aws:sns:us-east-1:...` |

---

## 📢 Notifications

### Slack Integration

Enhanced Slack notifications with:

- **Color-coded alerts** (Red=Critical, Orange=High, Yellow=Medium, Green=Success)
- **Drift summary** with counts (Total Resources, Drifted Resources, Critical Issues)
- **Top 5 drifted resources** prioritized by severity score
- **Success messages** when no drift detected
- **Direct link** to HTML report

**Example Slack Message:**

```
🔴 Terraform Drift Report: DEV
Severity: HIGH

Total Resources: 8
Drifted Resources: 3
Critical Issues: 1
High Severity Issues: 2

Top Drifts (Priority):
🔥 aws_security_group.web (MODIFY)
⚠️ aws_instance.app_server (MODIFY)
⚠️ aws_s3_bucket.data (MODIFY)

View full report: file:///path/to/reports/drift_report_*.html
```

### SNS/Email Notifications

Text-based notifications for critical and high-severity drift:

```
Subject: Terraform Drift - CRITICAL

Drift Detection Summary:
- Environment: production
- Drifted Resources: 5
- Highest Severity: critical
- Critical Issues: 2
- High Issues: 3

View detailed report: [Link]
```

---

## 📊 Reporting

### HTML Dashboard

Interactive visual reports with:

- **Chart.js doughnut chart** showing severity distribution
- **Responsive design** for mobile and desktop
- **Severity badges** color-coded by level
- **Detailed drift table** with resource address, type, change, and details

**Report Location:** `reports/index.html` (latest) and `reports/drift_report_TIMESTAMP.html`

### JSON Export

Machine-readable format for integration:

```json
{
  "summary": {
    "environment": "dev",
    "timestamp": "2026-01-09T20:33:07",
    "total_resources": 8,
    "drifted_resources": 3,
    "drift_percentage": 37.5,
    "critical_count": 1,
    "high_count": 2,
    "medium_count": 0,
    "low_count": 0
  },
  "drifts": [
    {
      "resource_address": "aws_security_group.web",
      "resource_type": "aws_security_group",
      "change_type": "update",
      "severity": "critical",
      "score": 4,
      "attribute": "ingress",
      "details": "Security rule modified"
    }
  ]
}
```

### Dependency Graph

Generated DOT file for Graphviz visualization:

```bash
# View dependencies
cat reports/dependencies.dot

# Generate PNG (requires Graphviz)
dot -Tpng reports/dependencies.dot -o reports/dependencies.png
open reports/dependencies.png
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Slack Notifications Not Working

**Symptom:** `Failed to send Slack notification: Invalid URL`

**Solution:**
```bash
# Check config/.env
cat config/.env | grep SLACK_WEBHOOK_URL

# Should show real webhook, not ${SLACK_WEBHOOK_URL}
# If incorrect, update:
echo "SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/ACTUAL/URL" >> config/.env
```

#### 2. DynamoDB Table Not Found

**Symptom:** `ResourceNotFoundException: Requested resource not found`

**Solution:**
```bash
# Create DynamoDB table
aws dynamodb create-table \
  --table-name terraform-drift-history \
  --attribute-definitions \
    AttributeName=scan_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=scan_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

#### 3. S3 Backend Bucket Errors

**Symptom:** `Error: Failed to get existing workspaces`

**Solution:**
```bash
# List buckets
aws s3 ls | grep terraform-state

# If bucket doesn't exist, create one:
BUCKET_NAME="terraform-state-drift-detector-$(date +%s)"
aws s3 mb s3://${BUCKET_NAME} --region us-east-1

# Update backend in terraform/environments/dev/main.tf
# Then reinitialize:
cd terraform/environments/dev
terraform init -reconfigure
```

#### 4. Permission Denied on Cron Script

**Symptom:** Cron job not executing

**Solution:**
```bash
# Make script executable
chmod +x scripts/run_drift_scan.sh

# Verify cron entry
crontab -l

# Test manually
./scripts/run_drift_scan.sh
```

---

## 🔬 Advanced Topics

### Custom Severity Rules

Extend `config/severity_rules.yaml` with your organization's standards:

```yaml
severity:
  critical:
    - aws_security_group
    - aws_iam_*        # Wildcards supported
    - "*_kms_*"
    - custom_module.database
```

### Policy-Based Filtering

Configure `modules/policy_engine.py` to ignore expected drift:

```python
# Example: Ignore auto-scaling group instance counts
policies:
  ignore_resources:
    - "aws_autoscaling_group.*.desired_capacity"
  
  critical_resources:
    - "aws_security_group.*"
    - "module.database.*"
```

### Multi-Environment Scanning

```bash
# Scan all environments
for env in dev staging prod; do
  python enhanced_drift_detector.py \
    --environment $env \
    --terraform-dir ./terraform/environments/$env
done
```

### AWS EventBridge Integration (Alternative to Cron)

```bash
# Create EventBridge rule
aws events put-rule \
  --name drift-detector-schedule \
  --schedule-expression "rate(6 hours)" \
  --state ENABLED

# Add target (Lambda function to invoke detector)
aws events put-targets \
  --rule drift-detector-schedule \
  --targets "Id"="1","Arn"="arn:aws:lambda:..."
```

---

## 📂 Project Structure

```
devops-drift-detector/
├── .github/
│   └── workflows/
│       └── drift_scan.yml           # CI/CD pipeline
│
├── config/
│   ├── config.yaml                  # Main configuration
│   ├── severity_rules.yaml          # Resource severity mappings
│   └── .env                         # Environment variables (gitignored)
│
├── modules/                         # Core Python modules
│   ├── terraform_client.py          # Terraform operations wrapper
│   ├── drift_analyzer.py            # Drift detection logic
│   ├── policy_engine.py             # Smart filtering engine
│   ├── severity_scorer.py           # Severity classification
│   ├── history_tracker.py           # DynamoDB persistence
│   ├── notifications.py             # Slack/SNS/Email alerts
│   ├── report_generator.py          # HTML/JSON report generation
│   └── dependency_mapper.py         # Resource graph generation
│
├── scripts/
│   └── run_drift_scan.sh            # Cron wrapper script
│
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   │   ├── main.tf              # Dev environment config
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── staging/                 # (Optional)
│   │   └── prod/                    # (Optional)
│   │
│   └── modules/
│       ├── networking/              # VPC, subnets, security groups
│       └── compute/                 # EC2, S3, app resources
│
├── reports/                         # Generated reports (gitignored)
│   ├── index.html                   # Latest report
│   ├── drift_report_*.html          # Historical reports
│   └── dependencies.dot             # Dependency graph
│
├── logs/                            # Log files (gitignored)
│   └── cron.log                     # Cron execution logs
│
├── enhanced_drift_detector.py       # Main entry point
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
└── .gitignore
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/devops-drift-detector.git
cd devops-drift-detector

# Create feature branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r drift-detector/requirements.txt
pip install pytest black pylint

# Run tests
pytest tests/

# Format code
black modules/ enhanced_drift_detector.py

# Lint
pylint modules/
```

### Pull Request Process

1. **Create a feature branch** from `main`
2. **Write tests** for new functionality
3. **Update documentation** (README, docstrings)
4. **Run linters** and ensure code quality
5. **Submit PR** with clear description of changes
6. **Address review comments**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **HashiCorp Terraform** - Infrastructure as Code platform
- **AWS** - Cloud infrastructure provider
- **Chart.js** - JavaScript charting library
- **Python Community** - Amazing ecosystem and tools

---

## 📚 Additional Resources

### Documentation

- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Related Projects

- [terraform-compliance](https://terraform-compliance.com/) - BDD-style compliance testing
- [tfsec](https://github.com/aquasecurity/tfsec) - Static analysis security scanner
- [terraformer](https://github.com/GoogleCloudPlatform/terraformer) - Import existing infrastructure

---

## 📞 Support

For issues, questions, or feature requests:

1. **Check Documentation** - Review this README and troubleshooting section
2. **Search Issues** - Look for similar problems in [GitHub Issues](https://github.com/JEGSON/devops-drift-detector/issues)
3. **Open New Issue** - Provide detailed information (error messages, configuration, steps to reproduce)
4. **Discussions** - Join community discussions for general questions

---

## 🎯 Roadmap

### Upcoming Features

- [ ] **Multi-Cloud Support** - Azure, GCP drift detection
- [ ] **Web Dashboard** - React-based UI for drift monitoring
- [ ] **Machine Learning** - Predict drift patterns
- [ ] **Auto-Remediation** - Automatically apply fixes for low-risk drift
- [ ] **Compliance Reporting** - SOC2, HIPAA, PCI-DSS compliance checks
- [ ] **Terraform Cloud Integration** - Native TFC/TFE support

---

**Built with ❤️ by DevOps Engineers, for DevOps Engineers**

**Live Demo:** [View Sample Report](reports/index.html)  
**GitHub:** [JEGSON/devops-drift-detector](https://github.com/JEGSON/devops-drift-detector)