# AWS Cloud Internship Project: Video Presentation & Viva Defense Script
## Student Internship Portal & Enterprise Cloud Architecture

**Developer:** Madhumitha A  
**Role:** AWS Cloud Architect & Full-Stack DevOps Specialist Intern  
**Project Repository:** [https://github.com/madhumitha19022-spec/AWS-internship](https://github.com/madhumitha19022-spec/AWS-internship)  
**Target Duration:** 3 to 5 Minutes  

---

## 🎬 Video Recording Guide (What to Show on Screen)

Record your screen using OBS Studio, Zoom, or Windows Game Bar (`Win + G`).  
Open your running portal in your browser: `http://127.0.0.1:5000` (or your deployed cloud URL) and follow the 6 scenes below:

---

### Scene 1: Introduction & Title Screen (0:00 - 0:45)
**Screen to Show:** Home Page (`/`) showing the hero banner with the live status pill.

**What to Say (English):**
> "Hello everyone, my name is **Madhumitha A**. Today, I am excited to present my AWS Cloud Computing Internship Capstone Project titled: **AWS Cloud Project: Custom VPC + EC2 Web Application + S3 Storage + IAM Roles + CloudWatch Monitoring + Automated Backup and Cost Control**.  
> The objective of this project is to build and deploy an enterprise-grade Student Internship Portal on Amazon Web Services, moving completely away from vulnerable default configurations to an isolated, secure, and monitored cloud architecture."

**What to Say (Tamil):**
> "அனைவருக்கும் வணக்கம், என் பெயர் **மதுமிதா ஏ**. எனது AWS Cloud Computing இன்டர்ன்ஷிப் ப்ராஜெக்ட்டான **Student Internship Portal and AWS Architecture**-ஐ உங்கள் முன் சமர்ப்பிப்பதில் மகிழ்ச்சி அடைகிறேன்.  
> இதன் முக்கிய நோக்கம், வழக்கமான default அமைப்புகளை தவிர்த்து, ஒரு பாதுகாப்பான **Custom AWS VPC**, Linux EC2 சர்வர், S3 ஸ்டோரேஜ், மற்றும் தானியங்கி கண்காணிப்புடன் கூடிய ஒரு முழுமையான கிளவுட் அப்ளிகேஷனை உருவாக்குவதாகும்."

---

### Scene 2: Operations Dashboard & Metrics (0:45 - 1:30)
**Screen to Show:** Dashboard Page (`/dashboard`) showing the 4 KPI cards and traffic graphs.

**What to Say (English):**
> "Navigating to our **Operations Dashboard**, we have real-time visibility into system health.  
> - Here we observe **750 Total Requests** analyzed, with **23 Unique Visitor IPs**.
> - The platform maintains a high **93.3% Success Rate** across HTTP 200 and cached responses.
> - We can see our **EC2 Server Status** reporting 2 out of 2 health checks passed.
> - And our **Amazon S3 Storage Card** showing private object bucket inventory, all protected under least-privilege IAM policies."

**What to Say (Tamil):**
> "இப்போது நாம் பார்ப்பது **Operations Dashboard**.  
> - இதில் மொத்தம் **750 வெப் ரிக்வெஸ்ட்கள்** மற்றும் **23 தனித்துவமான IP முகவரிகள்** பகுப்பாய்வு செய்யப்பட்டுள்ளன.
> - இதில் **93.3% வெற்றி விகிதம் (Success Rate)** பெறப்பட்டுள்ளது.
> - நமது **EC2 சர்வர் நிலை** மற்றும் **S3 ஸ்டோரேஜ் விவரங்கள்** இங்கு தெளிவாகக் காட்டப்படுகின்றன."

---

### Scene 3: Custom AWS VPC Network Architecture (1:30 - 2:30)
**Screen to Show:** Architecture & Project Info Page (`/project-info`) showing the high-resolution architecture diagram.

**What to Say (English):**
> "Here is our complete **AWS System Topology**:
> 1. **Custom VPC (`10.0.0.0/16`)**: We created an isolated private virtual cloud with 65,000+ available addresses.
> 2. **Public Subnet (`10.0.1.0/24`)**: Configured with an **Internet Gateway (`internship-igw`)** and a custom route table directing traffic `0.0.0.0/0` to the gateway.
> 3. **Security Group (`internship-web-sg`)**: Inbound web traffic is strictly permitted on Port 80, while administrative SSH is locked down strictly to Port 22.
> 4. **Zero Hardcoded Secrets**: Unlike amateur deployments, our EC2 instance uses an **IAM Instance Profile (`EC2-Internship-Portal-Role`)**. It dynamically fetches temporary STS security tokens—zero AWS access keys exist in our code."

**What to Say (Tamil):**
> "இதுவே நமது **AWS Architecture**:  
> 1. **Custom VPC (10.0.0.0/16)** மூலம் தனித்துவமான நெட்வொர்க் உருவாக்கப்பட்டுள்ளது.  
> 2. **Public Subnet (10.0.1.0/24)** மற்றும் **Internet Gateway** மூலம் பாதுகாப்பான ரூட்டிங் செய்யப்பட்டுள்ளது.  
> 3. **Security Group** வழியாக போர்ட் 80 மற்றும் 22 மட்டுமே திறக்கப்பட்டுள்ளது.  
> 4. மிக முக்கியமாக, எங்கள் கோடில் எந்தவித **AWS Access Key-களும் ஹார்ட்கோட் செய்யப்படவில்லை**. IAM Instance Role மூலமே EC2 அனைத்து சேவைகளையும் அணுகுகிறது."

---

### Scene 4: Log Analysis & Diagnostics Engine (2:30 - 3:30)
**Screen to Show:** Log Analysis Page (`/log-analysis`) showing the Chart.js hourly charts and error tables.

**What to Say (English):**
> "On the **Log Analysis Page**, our custom Python engine parses 750 realistic server access logs:
> - **Peak Traffic Identification:** Traffic peaks at **13:00 UTC** with 75 requests.
> - **Error Diagnostics:** It categorizes **39 client errors (4xx)** like unauthorized paths and 404s, and **11 server errors (5xx)**.
> - An interactive filter allows administrators to drill down into logs by status code or request method in real time."

**What to Say (Tamil):**
> "அடுத்து நமது **Log Analysis** பக்கம். நமது பிரத்யேக பைத்தான் அனலைசர் 750 லாக் பதிவுகளை ஆராய்ந்து:  
> - மதியம் 1 மணிக்கு அதிகபட்ச டிராஃபிக் (Peak hour) ஏற்படுவதை கண்டறிந்துள்ளது.  
> - 4xx மற்றும் 5xx எரர்களை துல்லியமாக வகைப்படுத்தி interactive சார்ட்டுகளாக வழங்குகிறது."

---

### Scene 5: Monitoring, Backups & Cost Control (3:30 - 4:15)
**Screen to Show:** AWS Monitoring Page (`/aws-monitoring`) showing CloudWatch alarms and S3 PutObject test.

**What to Say (English):**
> "In the **AWS Monitoring Center**:
> - We configured **Amazon CloudWatch Alarms** that trigger if CPU utilization exceeds 70% or if EC2 hardware status checks fail.
> - Alarms automatically trigger **Amazon SNS**, dispatching instant email alerts to `madhumitha19022@gmail.com`.
> - **Disaster Recovery:** We scripted automated **EBS root volume snapshots** for rapid restore drills.
> - **Cost Control:** We enforced a strict **$1.00 USD monthly AWS Budget** with alerts, deliberately avoiding expensive NAT Gateways and ALBs to remain 100% Free Tier compliant."

**What to Say (Tamil):**
> "நமது **AWS Monitoring** பக்கத்தில்:  
> - CPU பயன்பாடு 70%-க்கு மேல் சென்றால் உடனடியாக இமெயில் அலர்ட் அனுப்ப **CloudWatch & Amazon SNS** இணைக்கப்பட்டுள்ளது.  
> - அவசர கால மீட்பிற்காக **EBS Volume Snapshot Backup** எடுக்கப்பட்டுள்ளது.  
> - எந்தவித கூடுதல் கட்டணமும் வராமல் தடுக்க **AWS Budgets** மூலம் $1.00 டாலர் வரம்பு நிர்ணயிக்கப்பட்டுள்ளது."

---

### Scene 6: Conclusion & GitHub Repository (4:15 - 4:45)
**Screen to Show:** GitHub Repository ([madhumitha19022-spec/AWS-internship](https://github.com/madhumitha19022-spec/AWS-internship)).

**What to Say (English):**
> "In conclusion, this project successfully fulfills all requirements of enterprise cloud architecture: custom networking, least-privilege security, automated alerting, disaster recovery, and data diagnostics.  
> All 32 project files, automated CloudFormation templates, and test suites are version-controlled on GitHub under **`madhumitha19022-spec/AWS-internship`**.  
> Thank you!"

**What to Say (Tamil):**
> "முடிவாக, ஒரு நிறுவன தரத்திலான AWS கிளவுட் அப்ளிகேஷனுக்கு தேவையான அனைத்து அம்சங்களும் வெற்றிகரமாக முடிக்கப்பட்டு, முழு சோர்ஸ் கோடும் GitHub-ல் புஷ் செய்யப்பட்டுள்ளது. நன்றி!"

---

## 🎯 Top 5 Viva / Interview Questions & Answers

**Q1: Why did you create a Custom VPC instead of using the Default VPC?**  
*Answer:* Default VPCs have public subnets across all AZs with open routing, which can expose internal resources. A Custom VPC gives us complete control over network boundaries, CIDR segmentation (`10.0.0.0/16`), custom route tables, and strict ingress rules.

**Q2: Why are IAM Roles safer than storing AWS Access Keys in code or `.env`?**  
*Answer:* IAM Instance Profiles issue temporary STS credentials that rotate automatically every few hours. Storing static access keys risks catastrophic leaks if pushed to GitHub or compromised on disk.

**Q3: How does the application handle reverse proxying on EC2?**  
*Answer:* Nginx acts as a high-performance reverse proxy listening on Port 80 and passes incoming HTTP requests internally to Gunicorn WSGI running on `127.0.0.1:5000` managed as a `systemd` daemon.

**Q4: What CloudWatch alarms did you configure?**  
*Answer:* Two alarms: `Internship-High-CPU-Alarm` triggering when EC2 `CPUUtilization > 70%` for 5 minutes, and `Internship-StatusCheckFailed-Alarm` triggering when status checks fail, both notifying an Amazon SNS email topic.

**Q5: How did you ensure zero unexpected AWS charges?**  
*Answer:* We adhered strictly to the Free Tier by using micro instances (`t2.micro`), configured an AWS Budget with $1.00 USD threshold notifications, and deliberately avoided costly resources like NAT Gateways ($32/month) and Application Load Balancers ($18/month).
