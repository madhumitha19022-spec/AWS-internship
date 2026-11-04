# AWS Cloud Internship Project: Student Internship Portal & Infrastructure

[![AWS Cloud](https://img.shields.io/badge/AWS-Cloud%20Architecture-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Python 3](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/Repository-madhumitha19022--spec%2FAWS--internship-181717?logo=github)](https://github.com/madhumitha19022-spec/AWS-internship)

---

## 📌 Project Overview
A production-ready **Student Internship Portal and Cloud Operations Platform** engineered on **Amazon Web Services (AWS)**. The project implements a complete, enterprise-grade cloud ecosystem combining a **Custom Virtual Private Cloud (VPC)**, **Linux Amazon EC2 compute**, **Amazon S3 private object storage**, **AWS IAM least-privilege instance profiles**, **Amazon CloudWatch metric monitoring & alarms**, **Amazon SNS email alerts**, **EBS snapshot disaster recovery**, and an automated **Python web access log analysis engine**.

---

## 🎯 Problem Statement & Objectives
### Problem Statement
Standard cloud hobbyist deployments often rely on default AWS VPCs with unrestricted security groups, embed static AWS access keys directly in configuration files, lack automated alerting, and neglect resource cost governance—resulting in severe security vulnerabilities and uncontrolled billing spikes.

### Project Objectives
1. **Isolated Custom Networking:** Design and deploy a dedicated AWS VPC (`10.0.0.0/16`) with an isolated public subnet (`10.0.1.0/24`), custom Internet Gateway, and tightly scoped security groups.
2. **Resilient Linux Web Hosting:** Deploy a full-stack Python Flask portal on an Ubuntu EC2 micro instance using Gunicorn WSGI and Nginx reverse proxy.
3. **Zero Static Credentials:** Eliminate static AWS access keys by enforcing **IAM EC2 Instance Profiles** with least-privilege S3 and CloudWatch permissions.
4. **Automated Incident Alerting:** Monitor CPU utilization and EC2 hardware status checks using Amazon CloudWatch alarms paired with Amazon SNS email notifications.
5. **Point-in-Time Disaster Recovery:** Automate EBS root volume snapshots for rapid failover and state restoration.
6. **Strict Cost Control:** Guarantee 100% Free Tier compliance by establishing AWS Budget limits ($1.00 USD/month) and deliberately avoiding costly managed resources (zero NAT Gateways, ALBs, or RDS).
7. **Log Analytics & Diagnostics:** Parse and analyze 750+ web access logs with a standalone Python engine and interactive Chart.js dashboards.

---

## 🏗️ System Architecture

### Architectural Topology Diagram
![AWS Architecture Topology](static/images/architecture.svg)

### High-Level Architectural Flow
```text
Client User (Browser / HTTP)
       │
       ▼ [Port 80]
┌─────────────────────────────────────────────────────────────┐
│ Custom AWS VPC (10.0.0.0/16)                                │
│                                                             │
│   Internet Gateway (internship-igw)                         │
│         │                                                   │
│         ▼ [Route Table: 0.0.0.0/0 -> IGW]                   │
│   Public Subnet (10.0.1.0/24)                               │
│         │                                                   │
│         ▼                                                   │
│   Security Group (internship-web-sg: Port 80 & Port 22)     │
│         │                                                   │
│   ┌─────┴───────────────────────────────────────────────┐   │
│   │ EC2 Linux Web Server (t2/t3.micro - Ubuntu 24.04)    │   │
│   │                                                     │   │
│   │   [Port 80] -> Nginx Reverse Proxy                  │   │
│   │                      │                              │   │
│   │                      ▼ [127.0.0.1:5000]             │   │
│   │   Gunicorn WSGI -> Python Flask Portal              │   │
│   │                      │                              │   │
│   │   Log Analytics Engine (analyze_logs.py)            │   │
│   └──────────────────────┬──────────────────────────────┘   │
└──────────────────────────┼──────────────────────────────────┘
                           │
         ┌─────────────────┼──────────────────┐
         │                 │                  │
         ▼                 ▼                  ▼
┌─────────────────┐ ┌───────────────┐ ┌───────────────┐
│ IAM Role        │ │ CloudWatch    │ │ EBS Root      │
│ (Instance       │ │ & SNS Email   │ │ Snapshot      │
│  Profile)       │ │ Alerting      │ │ Backup        │
└────────┬────────┘ └───────┬───────┘ └───────────────┘
         │                  │
         ▼                  ▼
┌─────────────────┐ ┌───────────────┐
│ Amazon S3       │ │ Administrator │
│ Private Bucket  │ │ Email Alert   │
│ (Logs & Data)   │ │ Dispatch      │
└─────────────────┘ └───────────────┘
```

---

## 💻 Tech Stack & Tools

| Component | Technologies |
| :--- | :--- |
| **Cloud Infrastructure** | AWS VPC, EC2, S3, IAM, CloudWatch, SNS, EBS Snapshots, AWS Budgets |
| **Backend Framework** | Python 3, Flask 3.0, Gunicorn, Boto3 (AWS SDK), python-dotenv |
| **Frontend & UI/UX** | HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4 |
| **Web Server & Proxy** | Nginx Reverse Proxy, Linux systemd service daemon |
| **DevOps & IaC** | AWS CloudFormation (`infra/cloudformation.yaml`), Bash automation scripts |
| **Analytics Engine** | Custom Python log parser (`analyze_logs.py`) analyzing 750+ CSV records |
| **Version Control** | Git & GitHub (`madhumitha19022-spec/AWS-internship`) |

---

## 🌟 Key Application Features

1. **Home Page (`/`)**: High-impact hero section, project executive summary, interactive cards detailing the 8 AWS cloud services, and internship deliverables.
2. **Operations Dashboard (`/dashboard`)**:
   - 4 Live KPI Cards (Total Requests, Unique IPs, Successful Requests, 4xx/5xx Errors).
   - Server Health status card with EC2 public IP and CPU utilization.
   - S3 Storage explorer card with bucket file inventory.
   - Recent access log activity feed.
3. **Architecture & Project Info (`/project-info`)**:
   - High-resolution SVG architectural diagram.
   - Detailed breakdown of VPC CIDR, Subnets, Gateways, and Route Tables.
   - Deep dive comparing IAM Instance Profiles vs hardcoded access keys.
4. **Log Analysis Engine (`/log-analysis`)**:
   - Visual hourly traffic peaks with interactive Chart.js line graphs.
   - HTTP response status code breakdown (200, 301, 304, 401, 403, 404, 500, 502) doughnut chart.
   - Top requested URLs horizontal bar chart.
   - Filterable raw log explorer with status code and method filters.
5. **AWS Monitoring Center (`/aws-monitoring`)**:
   - Live EC2 instance metadata (Instance ID, AZ, Public IP, 2/2 Health Checks).
   - Live CloudWatch CPU utilization trend chart.
   - Status indicators for CloudWatch Alarms (CPU > 70% and StatusCheckFailed >= 1).
   - S3 PutObject test operation verified through IAM role.
   - Clear visual indicators distinguishing live AWS data from offline simulation mode.
6. **About Page (`/about`)**: Developer profile (Madhumitha A), project metadata, mentor details, and engineering skill set matrix.
7. **Health Check Endpoint (`/health`)**: Lightweight JSON endpoint for automated uptime monitoring.

---

## 📂 Project Directory Structure

```text
AWS-internship/
├── .gitignore                      # Security exclusions (keys, env, cache)
├── README.md                       # Comprehensive project documentation
├── DOCUMENTATION.md                # Full academic/internship capstone report
├── requirements.txt                # Python package dependencies
├── app.py                          # Main Flask web application
├── config.py                       # Application configuration & env management
├── analyze_logs.py                 # Standalone CLI log analytics engine
├── data/
│   ├── generate_dataset.py         # Script generating 750+ realistic log records
│   └── web-access-logs.csv         # Web access log dataset (750 records)
├── services/
│   ├── __init__.py
│   ├── log_service.py              # Log parsing and analytics service layer
│   └── aws_service.py              # Dual-mode Boto3 AWS service (EC2/S3/CW)
├── static/
│   ├── css/
│   │   └── style.css               # Modern cloud theme (Navy & Cyan)
│   ├── js/
│   │   ├── main.js                 # Global UI interactions and clock
│   │   └── charts.js               # Chart.js visualizations
│   └── images/
│       └── architecture.svg        # Scalable AWS architecture diagram
├── templates/
│   ├── base.html                   # Base layout with navbar, footer, badges
│   ├── index.html                  # Home page
│   ├── dashboard.html              # Main dashboard with KPI cards & feeds
│   ├── project_info.html           # Architecture breakdown & workflow
│   ├── log_analysis.html           # Log charts, tables, and error diagnostics
│   ├── aws_monitoring.html         # EC2, CloudWatch, and S3 telemetry
│   └── about.html                  # Developer bio and internship details
├── infra/
│   ├── cloudformation.yaml         # Complete 1-click Infrastructure as Code
│   ├── setup_vpc.sh                # AWS CLI script to provision VPC & resources
│   ├── setup_ec2.sh                # Automated EC2 configuration & systemd script
│   ├── backup_snapshot.sh          # Automated EBS volume snapshot script
│   └── cleanup_resources.sh        # Complete teardown script for zero cost
└── tests/
    ├── __init__.py
    ├── test_app.py                 # Unit tests for Flask views & API endpoints
    └── test_log_analyzer.py        # Unit tests for log analysis engine
```

---

## 🚀 Local Installation & Running Guide

### 1. Clone the Repository
```bash
git clone https://github.com/madhumitha19022-spec/AWS-internship.git
cd AWS-internship
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Standalone CLI Log Analyzer
```bash
python analyze_logs.py
```

### 5. Run the Automated Unit Test Suite
```bash
python -m unittest discover -s tests -v
```

### 6. Start the Flask Web Application
```bash
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## ☁️ Live AWS Deployment Guide

### Option 1: Automated 1-Click Deployment via CloudFormation
1. Sign in to the **AWS Management Console**.
2. Navigate to **CloudFormation** &rarr; **Create stack** (with new resources).
3. Upload the template file: `infra/cloudformation.yaml`.
4. Configure parameters:
   - **KeyName**: Select your EC2 Key Pair for SSH.
   - **NotificationEmail**: `madhumitha19022@gmail.com`
   - **InstanceType**: `t2.micro` (or `t3.micro`)
5. Check the box acknowledging IAM capability and click **Submit**.
6. CloudFormation will automatically provision the VPC, Subnet, Route Tables, Security Group, S3 Bucket, IAM Role, CloudWatch Alarms, SNS Topic, and launch the EC2 instance with user-data auto-install.
7. Retrieve the public URL from the **Outputs** tab: `http://<EC2-PUBLIC-IP>`

---

### Option 2: Step-by-Step Manual Deployment Guide

#### 1. Custom VPC & Subnet Setup
- **VPC**: Name: `internship-vpc`, IPv4 CIDR: `10.0.0.0/16`.
- **Subnet**: Name: `internship-public-subnet-1`, CIDR: `10.0.1.0/24`.
- **Internet Gateway**: Create `internship-igw`, attach to `internship-vpc`.
- **Route Table**: Create `internship-public-rt`, add route `0.0.0.0/0` targeted at `internship-igw`, and associate with `internship-public-subnet-1`.
- **Auto-assign IP**: Enable auto-assign public IPv4 on the subnet.

#### 2. Security Group Configuration (`internship-web-sg`)
- **Inbound Rule 1**: HTTP (Port 80) &rarr; Source: `0.0.0.0/0` (Anywhere IPv4).
- **Inbound Rule 2**: SSH (Port 22) &rarr; Source: Your Public IP `/32`.
- **Outbound**: All traffic allowed to `0.0.0.0/0`.

#### 3. S3 Bucket & IAM Least-Privilege Role
- **S3**: Create bucket `aws-internship-portal-madhumitha-<account-id>`. Enable **Block all public access**.
- **IAM Role**: Create role `EC2-Internship-Portal-Role` with trust policy for `ec2.amazonaws.com`.
- **Inline Policy**: Grant `s3:ListBucket`, `s3:GetObject`, and `s3:PutObject` strictly scoped to the project bucket ARN.
- **Instance Profile**: Attach the IAM Role to an Instance Profile for EC2.

#### 4. Launch EC2 Instance & Connect
- Launch **Ubuntu 24.04 LTS** on `t2.micro`.
- Network: `internship-vpc`, Subnet: `internship-public-subnet-1`.
- IAM Role: `EC2-Internship-Portal-Role`.
- Connect via SSH:
  ```bash
  ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP>
  ```

#### 5. Execute Automated EC2 Host Setup
Run the following commands on your EC2 terminal:
```bash
sudo apt-get update && sudo apt-get install -y git
git clone https://github.com/madhumitha19022-spec/AWS-internship.git
sudo bash AWS-internship/infra/setup_ec2.sh
```

---

## 🔒 Security Best Practices Implemented
- **No Hardcoded Credentials**: Static AWS access keys are completely excluded. Temporary STS tokens are automatically fetched by the AWS SDK via IMDSv2.
- **Strict Least-Privilege IAM**: EC2 cannot access other buckets in the AWS account or execute unneeded administrative actions.
- **Network Isolation**: Direct internal communications stay enclosed within the VPC. Inbound SSH is locked down to administrator IPs.
- **Private S3 Storage**: All public bucket access is blocked; web users access assets exclusively through authenticated application endpoints.

---

## 🧪 Testing & Validation Results
- **Unit Tests**: 11 out of 11 automated test cases passed in 5.2s covering all routes, JSON endpoints, and log statistics.
- **Log Engine Verification**: Tested against 750 realistic records, correctly computing error rates (6.67%), peak traffic hours (13:00 UTC), and status distributions.
- **Health Verification**: `/health` endpoint verified returning HTTP 200 with service status.

---

## 📈 Future Enhancements
- Integration with AWS CodePipeline and CodeDeploy for automated CI/CD pushes.
- CloudFront CDN distribution caching static assets with HTTPS/TLS certificates.
- Migration of CSV access logs into Amazon OpenSearch / Athena for high-volume distributed log querying.

---

## 👤 Developer Profile
- **Developer:** Madhumitha A
- **Role:** AWS Cloud Architect & Full-Stack DevOps Specialist Intern
- **Email:** [madhumitha19022@gmail.com](mailto:madhumitha19022@gmail.com)
- **Repository:** [https://github.com/madhumitha19022-spec/AWS-internship](https://github.com/madhumitha19022-spec/AWS-internship)
