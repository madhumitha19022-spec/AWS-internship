# AWS Cloud Computing Internship Capstone Project Report
## Student Internship Portal & Enterprise Cloud Architecture

**Project Title:** AWS Cloud Project: Custom VPC + EC2 Web Application + S3 Storage + IAM Roles + CloudWatch Monitoring + Automated Backup and Cost Control  
**Developer:** Madhumitha A  
**Developer Contact:** madhumitha19022@gmail.com  
**Version Control:** [https://github.com/madhumitha19022-spec/AWS-internship](https://github.com/madhumitha19022-spec/AWS-internship)  
**Date:** November 2026  

---

## Table of Contents
1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Project Objectives](#4-project-objectives)
5. [Existing System vs Proposed System](#5-existing-system-vs-proposed-system)
6. [System Requirements](#6-system-requirements)
   - 6.1 [Hardware Requirements](#61-hardware-requirements)
   - 6.2 [Software Requirements](#62-software-requirements)
7. [AWS Architecture & Topology](#7-aws-architecture--topology)
8. [System Design & Component Architecture](#8-system-design--component-architecture)
9. [AWS Service Configuration](#9-aws-service-configuration)
   - 9.1 [Custom Virtual Private Cloud (VPC) & Subnets](#91-custom-virtual-private-cloud-vpc--subnets)
   - 9.2 [Amazon EC2 Compute & Reverse Proxy](#92-amazon-ec2-compute--reverse-proxy)
   - 9.3 [Amazon S3 Storage Architecture](#93-amazon-s3-storage-architecture)
   - 9.4 [AWS IAM Least-Privilege Security Roles](#94-aws-iam-least-privilege-security-roles)
   - 9.5 [Amazon CloudWatch & Amazon SNS Alerting](#95-amazon-cloudwatch--amazon-sns-alerting)
   - 9.6 [EBS Automated Snapshot Backup & Disaster Recovery](#96-ebs-automated-snapshot-backup--disaster-recovery)
   - 9.7 [AWS Budgets & Cost Governance](#97-aws-budgets--cost-governance)
10. [Web Access Log Analysis Engine](#10-web-access-log-analysis-engine)
11. [Testing and Verification](#11-testing-and-verification)
12. [Results and Key Outcomes](#12-results-and-key-outcomes)
13. [Conclusion](#13-conclusion)
14. [Future Enhancements](#14-future-enhancements)

---

## 1. Abstract
The rapid adoption of cloud computing has transformed modern application delivery. However, deploying applications using default cloud settings frequently leads to critical security exposures, unmonitored infrastructure, lack of disaster recovery, and uncontrolled billing overheads.

This project implements a secure, reliable, and cost-effective **Student Internship Portal** hosted on **Amazon Web Services (AWS)**. The entire cloud infrastructure is isolated inside a **Custom Virtual Private Cloud (VPC)** with defined CIDR blocks (`10.0.0.0/16`), a public subnet (`10.0.1.0/24`), custom route tables, and an Internet Gateway. Compute is handled by an **Amazon EC2 micro Linux instance** running a modular Python Flask application served through **Gunicorn** and reverse-proxied by **Nginx** on Port 80. Security is enforced through **AWS Identity and Access Management (IAM) Instance Profiles**, guaranteeing that zero AWS access keys are embedded in source code. Object storage is delegated to a private **Amazon S3 bucket** configured with Block Public Access. Continuous health and performance metrics are monitored through **Amazon CloudWatch**, which automatically dispatches alerts to administrators via **Amazon SNS**. Point-in-time disaster recovery is accomplished through **Elastic Block Store (EBS) automated volume snapshots**, while financial governance is maintained through **AWS Budgets** configured to eliminate unexpected charges. In addition, an analytical engine parses over 750 realistic web access logs to identify peak traffic periods, error distributions, and visitor metrics visualized through interactive dashboard charts.

---

## 2. Introduction
Cloud architecture demands more than simply deploying code to a virtual machine. Enterprise architectures require rigorous segmentation of networking layers, strict adherence to the principle of least privilege, persistent metric logging, automated incident alerting, and disaster mitigation plans.

The **Student Internship Portal** serves as an operational management platform and showcase of production-grade AWS practices. Developed during the AWS Cloud Architecture internship, this capstone project demonstrates the complete engineering lifecycle from network design, security policy formulation, and application development to DevOps automation, infrastructure testing, and cost control.

---

## 3. Problem Statement
In traditional and junior developer cloud setups:
1. **Network Vulnerability:** Applications are deployed in default VPCs across flat networks where internal resources share direct Internet exposure.
2. **Credential Compromise:** Developers frequently store static AWS Access Keys (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) in `.env` files or hardcoded scripts, leading to catastrophic key leakage and account compromise when committed to version control.
3. **Absence of Observability:** Infrastructure runs unmonitored until users complain of downtime, without metric thresholds or automated alerts for CPU spikes or system failures.
4. **Disaster Recovery Deficiency:** Lack of automated volume backups results in permanent data loss in the event of disk degradation or misconfiguration.
5. **Billing Shock:** Unrestricted provisioning of default NAT Gateways, Application Load Balancers, and managed databases easily causes unexpected monthly bills running into hundreds of dollars.

---

## 4. Project Objectives
- **Custom Networking:** Engineer a Custom AWS VPC with private addressing (`10.0.0.0/16`), custom route tables, Internet Gateway, and tightly scoped Security Groups.
- **Production Web Stack:** Deploy a Python Flask application on an Ubuntu Linux EC2 instance managed by `systemd` and Nginx.
- **Role-Based Security:** Enforce temporary token generation through IAM EC2 Instance Profiles, eliminating all hardcoded secrets.
- **Private S3 Storage:** Integrate private object storage for log archiving and datasets with least-privilege bucket policies.
- **CloudWatch & SNS Alerting:** Configure metric alarms for CPU utilization (>70%) and instance status check failures with email dispatch.
- **Automated EBS Backups:** Execute point-in-time snapshots of the EC2 root volume with documented recovery drill instructions.
- **Zero-Cost Free Tier Compliance:** Establish an AWS Budget of $1.00 USD/month and maintain zero chargeable resources (no NAT Gateways, ALBs, or RDS).
- **Log Analytics:** Build an automated CLI script and web dashboard for analyzing web access logs (750+ records) and visualizing error trends.

---

## 5. Existing System vs Proposed System

| Dimension | Existing / Hobbyist System | Proposed AWS Internship Architecture |
| :--- | :--- | :--- |
| **Network Isolation** | Default AWS VPC with default subnets | Dedicated Custom VPC (`10.0.0.0/16`) and subnet (`10.0.1.0/24`) |
| **Credential Security** | Static AWS Access Keys hardcoded or in `.env` | IAM Instance Profile with automatic STS temporary credential rotation |
| **Web Server Proxy** | Flask development server directly on port 5000 | Production Gunicorn WSGI behind Nginx reverse proxy on Port 80 |
| **Storage Security** | Public S3 buckets or local disk storage | Private S3 bucket with all 4 Block Public Access flags activated |
| **Monitoring** | Manual inspection without alarms | Amazon CloudWatch Alarms + Amazon SNS real-time email dispatch |
| **Backup & DR** | No volume backup | Point-in-time EBS root snapshots with documented restore procedures |
| **Cost Management** | Unmonitored, unexpected monthly charges | AWS Budgets with alerts at 80% and 100% threshold of $1.00 USD limit |

---

## 6. System Requirements

### 6.1 Hardware Requirements
- **Cloud Compute Host:** AWS EC2 `t2.micro` or `t3.micro` instance (1 vCPU, 1 GiB RAM).
- **Storage Volume:** 15 GiB General Purpose SSD (gp3) EBS root volume.
- **Local Development Machine:** 4 GB RAM minimum, 10 GB free disk space.

### 6.2 Software Requirements
- **Operating System:** Ubuntu 24.04 LTS (HVM) or Amazon Linux 2023.
- **Backend Runtime:** Python 3.10+ (Tested on Python 3.14).
- **Web Framework:** Flask 3.0+.
- **WSGI Application Server:** Gunicorn 21.2+.
- **Reverse Proxy:** Nginx 1.24+.
- **AWS SDK:** Boto3 1.34+.
- **Frontend Libraries:** Bootstrap 5.3, Bootstrap Icons 1.11, Chart.js 4.4.
- **Version Control:** Git 2.40+ and GitHub.

---

## 7. AWS Architecture & Topology
The application follows a tiered, cloud-native architecture:
1. **Perimeter Layer:** External users connect via standard HTTP (Port 80) directed at the EC2 Public IP.
2. **Networking Layer:** Custom VPC (`10.0.0.0/16`) isolates internal traffic. An Internet Gateway provides external egress/ingress mapped through a custom public route table to Subnet `10.0.1.0/24`.
3. **Compute Layer:** An Amazon EC2 Linux instance running Nginx receives web requests and routes them internally to Gunicorn listening on `127.0.0.1:5000`.
4. **Security Layer:** An IAM Role attached as an Instance Profile enables EC2 to interact with S3 and CloudWatch without keys.
5. **Data & Storage Layer:** Amazon S3 stores raw access logs, dataset archives, and media assets.
6. **Telemetry & Governance Layer:** CloudWatch gathers CPU and status checks; SNS sends email alerts; AWS Budgets monitors costs.

---

## 8. System Design & Component Architecture

### 8.1 MVC & Service Layer Design
```text
┌─────────────────────────────────────────────────────────────┐
│                       Templates (HTML5)                     │
│  index.html | dashboard.html | project_info.html            │
│  log_analysis.html | aws_monitoring.html | about.html       │
└──────────────────────────────▲──────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────┐
│                    Flask Controller (app.py)                │
│  Routes: /, /dashboard, /project-info, /log-analysis,       │
│          /aws-monitoring, /about, /health, /api/*           │
└──────────────▲──────────────────────────────▲───────────────┘
               │                              │
┌──────────────┴──────────────┐┌──────────────┴───────────────┐
│ Log Service & Parser        ││ AWS Boto3 Service            │
│ (services/log_service.py)   ││ (services/aws_service.py)    │
│ Statistical distributions   ││ EC2 IMDSv2, S3, CloudWatch   │
└──────────────▲──────────────┘└──────────────▲───────────────┘
               │                              │
┌──────────────┴──────────────┐┌──────────────┴───────────────┐
│ Dataset                     ││ AWS APIs / Simulation Engine │
│ (data/web-access-logs.csv)  ││ IAM STS, S3 API, CloudWatch  │
└─────────────────────────────┘└──────────────────────────────┘
```

---

## 9. AWS Service Configuration

### 9.1 Custom Virtual Private Cloud (VPC) & Subnets
- **VPC ID:** `internship-vpc`
- **IPv4 CIDR:** `10.0.0.0/16` (Provides 65,536 private IP addresses)
- **DNS Attributes:** `enableDnsHostnames=true`, `enableDnsSupport=true`
- **Subnet:** `internship-public-subnet-1`, CIDR `10.0.1.0/24` (256 addresses)
- **Internet Gateway:** `internship-igw` attached to VPC
- **Route Table:** `internship-public-rt`
  - Route Destination: `0.0.0.0/0` &rarr; Target: `internship-igw`
  - Subnet Association: Associated with `internship-public-subnet-1`

### 9.2 Amazon EC2 Compute & Reverse Proxy
- **Instance Type:** `t2.micro` (1 vCPU, 1 GB Memory, Free Tier Eligible)
- **Security Group:** `internship-web-sg`
  - Inbound Rule 1: HTTP Port 80 from `0.0.0.0/0`
  - Inbound Rule 2: SSH Port 22 from Administrator IP
  - Outbound Rule: All traffic allowed to `0.0.0.0/0`
- **Application Daemon (`systemd`):** `/etc/systemd/system/internship-portal.service` running 3 Gunicorn workers.
- **Nginx Reverse Proxy:** Reverse proxies public port 80 traffic to internal `127.0.0.1:5000`.

### 9.3 Amazon S3 Storage Architecture
- **Bucket Name:** `aws-internship-portal-madhumitha-<account-id>`
- **Access Level:** Private. Block Public Access enabled across all four categories:
  - `BlockPublicAcls = true`
  - `IgnorePublicAcls = true`
  - `BlockPublicPolicy = true`
  - `RestrictPublicBuckets = true`
- **Encryption:** AES-256 Server-Side Encryption (`aws:kms` or `AES256`).

### 9.4 AWS IAM Least-Privilege Security Roles
- **Role Name:** `EC2-Internship-Portal-Role`
- **Trust Relationship:** `ec2.amazonaws.com`
- **Policy Statement:**
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": ["s3:ListBucket"],
        "Resource": "arn:aws:s3:::aws-internship-portal-madhumitha-*"
      },
      {
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Resource": "arn:aws:s3:::aws-internship-portal-madhumitha-*/*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "cloudwatch:PutMetricData",
          "cloudwatch:GetMetricData",
          "cloudwatch:DescribeAlarms",
          "ec2:DescribeInstances"
        ],
        "Resource": "*"
      }
    ]
  }
  ```

### 9.5 Amazon CloudWatch & Amazon SNS Alerting
- **Alarm 1: High CPU Utilization (`Internship-High-CPU-Alarm`)**
  - Metric: `AWS/EC2 -> CPUUtilization`
  - Threshold: `> 70%` for 1 consecutive period of 300 seconds (5 minutes).
  - Action: Dispatches notification to SNS Topic `internship-alerts-topic`.
- **Alarm 2: Status Check Failed (`Internship-StatusCheckFailed-Alarm`)**
  - Metric: `AWS/EC2 -> StatusCheckFailed`
  - Threshold: `>= 1` for 60 seconds (1 minute).
  - Action: Dispatches notification to SNS Topic `internship-alerts-topic`.
- **SNS Topic:** `internship-alerts-topic` with protocol `email` subscribed to `madhumitha19022@gmail.com`.

### 9.6 EBS Automated Snapshot Backup & Disaster Recovery
- **Snapshot Script:** `infra/backup_snapshot.sh`
- **Snapshot Tagging:** `Name: Internship-Portal-Root-Backup`, `Project: AWS-Internship-Portal`.
- **Restoration Drill:**
  1. Identify backup snapshot ID from AWS Console or CLI:
     ```bash
     aws ec2 describe-snapshots --filters "Name=tag:Name,Values=Internship-Portal-Root-Backup"
     ```
  2. Create a replacement EBS volume in the same Availability Zone.
  3. Stop the damaged EC2 instance, detach corrupted volume, and attach the newly created volume as `/dev/sda1`.
  4. Start the instance; the web application and all dependencies immediately resume operating identically.

### 9.7 AWS Budgets & Cost Governance
- **Budget Amount:** $1.00 USD / Monthly.
- **Threshold 1:** Alert sent via email when forecasted/actual spend reaches 80% ($0.80).
- **Threshold 2:** High-priority warning alert sent when actual spend reaches 100% ($1.00).
- **Cost Minimization Checklist:**
  - [x] Zero NAT Gateways provisioned ($32.40/month baseline saved).
  - [x] Zero Application Load Balancers ($18.00/month baseline saved).
  - [x] Zero Amazon RDS database instances ($14.00/month baseline saved).
  - [x] EC2 instance restricted to `t2.micro` or `t3.micro` within the 750 hours/month Free Tier allocation.
  - [x] S3 storage scoped under 5 GB standard tier.

---

## 10. Web Access Log Analysis Engine
The system includes `analyze_logs.py` and `data/web-access-logs.csv` (750 realistic records spanning 24 hours).
- **Fields:** `timestamp`, `ip`, `method`, `path`, `status`, `bytes`, `user_agent`.
- **Metrics Calculated:**
  - Total requests: 750
  - Unique visitor IP addresses: 23
  - Successful requests (2xx/3xx): 700 (93.33%)
  - Client errors (4xx): 39 (5.20%)
  - Server errors (5xx): 11 (1.47%)
  - Peak traffic hour: 13:00 UTC (75 requests)
  - Total bandwidth transferred: 14.25 MB

---

## 11. Testing and Verification
Automated test suite located in `tests/`:
- `tests/test_log_analyzer.py`: Validates calculation logic for peak hours, error rate categorization, and CSV parser integrity.
- `tests/test_app.py`: Validates that all six web views (`/`, `/dashboard`, `/project-info`, `/log-analysis`, `/aws-monitoring`, `/about`), the health check (`/health`), and REST endpoints (`/api/logs/summary`, `/api/aws/status`) respond with HTTP 200 OK.
- **Test Execution Result:**
  ```text
  Ran 11 tests in 5.201s
  OK
  ```

---

## 12. Results and Key Outcomes
1. **Fully Functional Multi-Page Web Application:** Responsive, high-performance portal featuring 6 complete views built with modern HTML5, CSS3, Bootstrap 5, and Chart.js.
2. **Zero Credentials Compromise:** Complete absence of AWS access keys in git repository or runtime code.
3. **Automated Infrastructure as Code:** `infra/cloudformation.yaml` provisions the complete multi-service stack with a single click.
4. **Resilient Production Stack:** Nginx + Gunicorn + `systemd` architecture providing automated service restarts upon failure.
5. **Observability & Backup:** CloudWatch and SNS alerts configured; EBS snapshot disaster recovery procedure verified.

---

## 13. Conclusion
The AWS Cloud Internship Project successfully achieves all architectural and functional goals outlined in the internship mandate. By combining custom VPC network isolation, least-privilege IAM instance roles, automated CloudWatch alerting, EBS point-in-time snapshots, and rigorous cost governance, the project serves as an exemplary showcase of enterprise cloud architecture and DevOps excellence.

---

## 14. Future Enhancements
1. **CI/CD Pipeline:** Implement GitHub Actions or AWS CodePipeline to automatically build, test, and deploy code updates to EC2 upon git push.
2. **Global CDN Acceleration:** Attach an Amazon CloudFront distribution to cache static assets globally and terminate SSL/TLS certificates via AWS Certificate Manager (ACM).
3. **Containerization:** Package the application using Docker and deploy on AWS Elastic Container Service (ECS) Fargate for serverless container execution.
