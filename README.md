# DevOps Configuration Drift Detector

A comprehensive Infrastructure-as-Code (IaC) drift detection system built with Terraform and Python, featuring automated CI/CD pipelines for detecting and alerting on manual infrastructure changes.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [CI/CD Workflows](#cicd-workflows)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

Configuration drift occurs when infrastructure resources are modified manually outside of Infrastructure-as-Code (IaC) tooling, causing the actual state to diverge from the declared state. This project provides:

- **Terraform-managed AWS infrastructure** across multiple environments
- **Automated drift detection** using Python
- **CI/CD pipelines** with GitHub Actions for validation and deployment
- **Automated alerting** when drift is detected
- **Comprehensive reporting** with console and JSON outputs

---

## 🏗️ Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Developer Workstation                    │
│              (Infrastructure Changes via Git)                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Git Repository                         │
│                         (GitHub)                             │
│                  Single Source of Truth                      │
└─────┬──────────────────────────────────────────┬────────────┘
      │                                           │
      │ (PR triggers)                             │ (Merge/Schedule)
      ▼                                           ▼
┌─────────────────────┐              ┌─────────────────────────┐
│  Terraform Plan     │              │  Drift Detection        │
│  (GitHub Actions)   │              │  (GitHub Actions)       │
│                     │              │  Runs every 6 hours     │
│  - Validate         │              └──────────┬──────────────┘
│  - Plan             │                         │
│  - Comment on PR    │                         │ (Detects drift)
└─────────────────────┘                         ▼
                                     ┌─────────────────────────┐
                                     │  Alert & Report         │
┌─────────────────────┐              │  - GitHub Issues        │
│  Terraform Apply    │              │  - JSON Reports         │
│  (GitHub Actions)   │              │  - Artifacts            │
│                     │              └─────────────────────────┘
│  - Plan             │
│  - Apply            │
└─────┬───────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AWS Infrastructure                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Dev Environment                       │  │
│  │                                                       │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │    VPC      │  │  EC2 Instance│  │  S3 Bucket │ │  │
│  │  │             │  │  (t3.micro)  │  │            │ │  │
│  │  │ - Subnets   │  │              │  │ App Data   │ │  │
│  │  │ - IGW       │  │ Web Server   │  │            │ │  │
│  │  │ - Route     │  │              │  │            │ │  │
│  │  │   Tables    │  └──────────────┘  └────────────┘ │  │
│  │  │ - Security  │                                    │  │
│  │  │   Groups    │                                    │  │
│  │  └─────────────┘                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Terraform State Management                    │  │
│  │                                                       │  │
│  │  ┌──────────────┐         ┌──────────────┐          │  │
│  │  │  S3 Bucket   │         │  DynamoDB    │          │  │
│  │  │  (State)     │         │  (Locking)   │          │  │
│  │  └──────────────┘         └──────────────┘          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Drift Detection Flow

```
┌─────────────────────────────────────────┐
│  Scheduled Trigger (Every 6 hours)      │
│  OR Manual Trigger                      │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  GitHub Actions: Drift Detection        │
│                                         │
│  1. Checkout code                       │
│  2. Setup AWS credentials               │
│  3. Setup Terraform                     │
│  4. Setup Python environment            │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  Python Drift Detector                  │
│                                         │
│  For each environment:                  │
│    - Run terraform init                 │
│    - Run terraform plan                 │
│      (with -detailed-exitcode)          │
│    - Parse plan output                  │
│    - Analyze drift                      │
│    - Generate reports                   │
└───────────────┬─────────────────────────┘
                │
                ▼
        ┌───────┴──────┐
        │              │
        ▼              ▼
┌──────────────┐  ┌──────────────┐
│ Exit Code 0  │  │ Exit Code 2  │
│ No Drift     │  │ Drift Found! │
└──────┬───────┘  └──────┬───────┘
       │                 │
       │                 ▼
       │      ┌─────────────────────┐
       │      │ Create GitHub Issue │
       │      │ - Title: 🚨 Drift   │
       │      │ - Details           │
       │      │ - Labels            │
       │      └─────────────────────┘
       │                 │
       │                 ▼
       │      ┌─────────────────────┐
       │      │ Upload Artifacts    │
       │      │ - JSON reports      │
       │      │ - Console output    │
       │      └─────────────────────┘
       │                 │
       └────────┬────────┘
                ▼
        ┌──────────────┐
        │  Workflow    │
        │  Complete    │
        └──────────────┘
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Drift Detection System                     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Python Application                     │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │   main.py    │→ │  config.yaml │               │    │
│  │  │ (Orchestrator)│  │ (Settings)   │               │    │
│  │  └──────┬───────┘  └──────────────┘               │    │
│  │         │                                          │    │
│  │         ▼                                          │    │
│  │  ┌──────────────────────────────────────────┐    │    │
│  │  │      terraform_client.py                  │    │    │
│  │  │  - init()                                 │    │    │
│  │  │  - plan()                                 │    │    │
│  │  │  - parse_plan_output()                    │    │    │
│  │  └──────────────┬───────────────────────────┘    │    │
│  │                 │                                 │    │
│  │                 ▼                                 │    │
│  │  ┌──────────────────────────────────────────┐    │    │
│  │  │      drift_analyzer.py                    │    │    │
│  │  │  - analyze_drift()                        │    │    │
│  │  │  - calculate_severity()                   │    │    │
│  │  │  - generate_recommendations()             │    │    │
│  │  └──────────────┬───────────────────────────┘    │    │
│  │                 │                                 │    │
│  │                 ▼                                 │    │
│  │  ┌──────────────────────────────────────────┐    │    │
│  │  │          Reporters                        │    │    │
│  │  │                                           │    │    │
│  │  │  ┌─────────────────┐  ┌──────────────┐  │    │    │
│  │  │  │ console_reporter│  │json_reporter │  │    │    │
│  │  │  │ - Colored output│  │ - JSON files │  │    │    │
│  │  │  └─────────────────┘  └──────────────┘  │    │    │
│  │  └──────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Core Features
- ✅ **Multi-Environment Support** - Separate dev, staging, and production environments
- ✅ **Automated Drift Detection** - Runs every 6 hours automatically
- ✅ **Manual Drift Detection** - Run on-demand via CLI or GitHub Actions
- ✅ **Comprehensive Reporting** - Console output with colors and JSON reports
- ✅ **Severity Classification** - Categorizes drift as Critical, Warning, or Info
- ✅ **GitHub Integration** - Creates issues automatically when drift is detected

### Infrastructure Features
- ✅ **Modular Terraform Design** - Reusable networking and compute modules
- ✅ **Remote State Management** - S3 backend with DynamoDB locking
- ✅ **Free Tier Optimized** - Designed to run within AWS free tier limits
- ✅ **Security Best Practices** - Proper security groups, IAM roles, encryption

### CI/CD Features
- ✅ **PR Validation** - Automatic `terraform plan` on pull requests
- ✅ **Automated Deployment** - Apply changes on merge to main branch
- ✅ **Scheduled Drift Checks** - Regular automated drift detection
- ✅ **Artifact Storage** - Drift reports saved for 30 days

---

## 📦 Prerequisites

### Required Tools
- **AWS Account** with free tier access
- **Terraform** >= 1.6.0
- **Python** >= 3.11
- **Git** and **GitHub** account
- **AWS CLI** configured with credentials

### AWS Permissions Required
- EC2 (create/modify instances, security groups)
- VPC (create/modify VPC, subnets, route tables)
- S3 (create/modify buckets)
- DynamoDB (create/modify tables)
- IAM (read-only for state management)

---

## 📁 Project Structure

```
devops-drift-detector/
├── README.md
├── .gitignore
│
├── terraform/
│   ├── backend/                      # State backend setup
│   │   ├── main.tf
│   │   └── variables.tf
│   │
│   ├── modules/                      # Reusable modules
│   │   ├── networking/
│   │   │   ├── main.tf              # VPC, subnets, IGW, security groups
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   │
│   │   └── compute/
│   │       ├── main.tf              # EC2 instances, S3 buckets
│   │       ├── variables.tf
│   │       └── outputs.tf
│   │
│   └── environments/                 # Environment-specific configs
│       └── dev/
│           ├── main.tf              # Environment composition
│           ├── variables.tf
│           ├── outputs.tf
│           └── terraform.tfstate    # (if using local state)
│
├── drift-detector/                   # Python drift detection tool
│   ├── main.py                      # Main orchestrator
│   ├── terraform_client.py          # Terraform operations wrapper
│   ├── drift_analyzer.py            # Drift analysis logic
│   ├── config.yaml                  # Local configuration
│   ├── config.ci.yaml               # CI/CD configuration
│   ├── requirements.txt             # Python dependencies
│   │
│   ├── reporters/                   # Output formatters
│   │   ├── console_reporter.py     # Colored console output
│   │   └── json_reporter.py        # JSON file reports
│   │
│   └── reports/                     # Generated reports (gitignored)
│       └── *.json
│
└── .github/
    └── workflows/                    # CI/CD pipelines
        ├── terraform-plan.yml       # PR validation
        ├── terraform-apply.yml      # Deployment
        └── drift-detection.yml      # Scheduled drift checks
```

---

## 🚀 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/devops-drift-detector.git
cd devops-drift-detector
```

### Step 2: Configure AWS Credentials

```bash
# Configure AWS CLI
aws configure

# Verify credentials
aws sts get-caller-identity
```

### Step 3: Create Terraform State Backend

```bash
cd terraform/backend

# Initialize and create state backend
terraform init
terraform apply

# Note the output values (bucket name, DynamoDB table)
```

### Step 4: Update Backend Configuration

Edit `terraform/environments/dev/main.tf` and update the backend block with your actual S3 bucket name from Step 3.

### Step 5: Deploy Dev Environment

```bash
cd ../environments/dev

# Initialize Terraform with remote backend
terraform init

# Review the plan
terraform plan

# Deploy infrastructure
terraform apply
```

### Step 6: Set Up Python Drift Detector

```bash
cd ../../../drift-detector

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Update config.yaml with your paths
# Test drift detection
python main.py
```

### Step 7: Configure GitHub Actions

1. **Add AWS credentials to GitHub Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Add: `AWS_ACCESS_KEY_ID`
   - Add: `AWS_SECRET_ACCESS_KEY`
   - Add: `AWS_REGION` (e.g., `us-east-1`)

2. **Push workflows to GitHub:**
```bash
git add .github/workflows/
git commit -m "Add CI/CD workflows"
git push origin main
```

---

## 💻 Usage

### Manual Drift Detection (Local)

```bash
cd drift-detector
source venv/bin/activate
python main.py
```

### Create Intentional Drift (For Testing)

1. Go to AWS Console → EC2 → Instances
2. Select your `dev-web-server` instance
3. Add a tag: `ManualChange = true`
4. Run drift detector again - it should detect the change!

### Fix Detected Drift

```bash
cd terraform/environments/dev
terraform apply  # This will remove the manual tag
```

### Trigger Drift Detection in CI/CD

1. Go to GitHub repository → Actions
2. Select "Drift Detection" workflow
3. Click "Run workflow"

### Create a Pull Request

```bash
# Make a change to infrastructure
git checkout -b feature/add-new-resource
echo '# New resource' >> terraform/environments/dev/main.tf

# Commit and push
git add .
git commit -m "Add new resource"
git push origin feature/add-new-resource

# Create PR on GitHub - Terraform plan will run automatically
```

---

## 🔄 CI/CD Workflows

### 1. Terraform Plan (Pull Request Validation)

**Trigger:** On pull request to `main` branch  
**Purpose:** Validate Terraform changes before merge

**Steps:**
1. Checkout code
2. Configure AWS credentials
3. Run `terraform fmt -check`
4. Run `terraform validate`
5. Run `terraform plan`
6. Post plan as PR comment

### 2. Terraform Apply (Deployment)

**Trigger:** On push to `main` branch OR manual trigger  
**Purpose:** Deploy infrastructure changes

**Steps:**
1. Checkout code
2. Configure AWS credentials
3. Run `terraform plan`
4. Run `terraform apply -auto-approve`
5. Output infrastructure details

### 3. Drift Detection (Scheduled)

**Trigger:** Every 6 hours OR manual trigger  
**Purpose:** Detect configuration drift

**Steps:**
1. Checkout code
2. Setup Python environment
3. Run drift detector
4. Upload reports as artifacts
5. Create GitHub issue if drift detected

---

## ⚙️ Configuration

### Drift Detector Configuration (`config.yaml`)

```yaml
# AWS Configuration
aws:
  region: us-east-1
  profile: default

# Terraform environments to monitor
terraform:
  environments:
    - name: dev
      path: /path/to/terraform/environments/dev
      enabled: true

# Detection settings
detection:
  check_interval_hours: 6
  ignore_resources: []
  ignore_attributes:
    - "tags.LastModified"
    - "metadata"

# Reporting options
reporting:
  formats:
    - console  # Colored terminal output
    - json     # JSON file reports
  output_dir: ./reports
  min_severity: info  # info, warning, critical

# Alerting (future enhancement)
alerting:
  enabled: false
```

### Terraform Variables

**Environment-specific:** `terraform/environments/dev/variables.tf`

```hcl
variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "dev"
}

variable "instance_type" {
  default = "t3.micro"  # Free tier eligible
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}
```

---

## 🔍 How It Works

### Drift Detection Algorithm

1. **Initialization**
   - Load configuration from `config.yaml`
   - Identify enabled environments

2. **For Each Environment**
   - Initialize Terraform (`terraform init`)
   - Run plan with detailed exit code (`terraform plan -detailed-exitcode`)
   - Parse exit code:
     - `0` = No changes (no drift)
     - `1` = Error
     - `2` = Changes detected (drift!)

3. **Drift Analysis**
   - Parse plan output to extract:
     - Resources to add
     - Resources to modify
     - Resources to destroy
   - Calculate severity:
     - **Critical:** Resources deleted manually
     - **Warning:** Multiple resources modified
     - **Info:** Minor changes

4. **Reporting**
   - Generate console report (colored output)
   - Save JSON report to disk
   - Upload to GitHub Actions artifacts (in CI)
   - Create GitHub issue if drift detected

5. **Recommendations**
   - Suggest running `terraform apply` to fix drift
   - Highlight critical issues (deletions)
   - Remind about IaC best practices

### Severity Levels

| Severity | Condition | Action Required |
|----------|-----------|-----------------|
| 🚨 **Critical** | Resources deleted manually | Immediate action - run terraform apply |
| ⚠️ **Warning** | 3+ resources modified | Review and apply soon |
| ℹ️ **Info** | Minor changes or additions | Review at convenience |

---

## 🐛 Troubleshooting

### Issue: Drift detector can't find Terraform directory

**Solution:** Update `config.yaml` with the correct absolute path:
```yaml
terraform:
  environments:
    - name: dev
      path: /absolute/path/to/terraform/environments/dev
```

### Issue: AWS credentials not working in GitHub Actions

**Solution:** Verify GitHub Secrets are set correctly:
- Repository → Settings → Secrets and variables → Actions
- Check `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are present

### Issue: Terraform plan fails with "instance type not eligible for free tier"

**Solution:** Use `t3.micro` or `t2.micro` instance type:
```hcl
variable "instance_type" {
  default = "t3.micro"
}
```

### Issue: State locking errors

**Solution:** Check DynamoDB table exists and has correct permissions:
```bash
aws dynamodb describe-table --table-name terraform-locks-drift-detector
```

### Issue: Drift detector shows no drift but infrastructure was changed

**Solution:** Ensure Terraform state is up to date:
```bash
cd terraform/environments/dev
terraform refresh
terraform plan
```

---

## 🎯 Future Enhancements

- [ ] **Slack Integration** - Send drift alerts to Slack channels
- [ ] **Auto-Remediation** - Automatically apply fixes for certain drift types
- [ ] **Multi-Environment** - Add staging and production environments
- [ ] **Dashboard** - Web UI for visualizing drift history
- [ ] **CloudWatch Metrics** - Send drift metrics to AWS CloudWatch
- [ ] **Webhook Support** - Trigger custom actions on drift detection
- [ ] **Email Notifications** - Send detailed reports via email
- [ ] **Drift Trends** - Track and analyze drift patterns over time

---

## 📚 Learning Resources

### Terraform
- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

### AWS
- [AWS Free Tier](https://aws.amazon.com/free/)
- [EC2 Documentation](https://docs.aws.amazon.com/ec2/)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---


---

## 🙏 Acknowledgments

- Terraform by HashiCorp
- AWS Cloud Platform
- GitHub Actions
- Python community

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Review existing issues for solutions

---

**Built with ❤️ for DevOps Engineers**