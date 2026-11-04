#!/bin/bash
# =============================================================================
# AWS Cloud Internship Project: Infrastructure Provisioning via AWS CLI
# =============================================================================
# Run this script with AWS CLI configured to provision all cloud resources.
# Region default: ap-south-1 (Mumbai) or us-east-1
# =============================================================================

set -e

AWS_REGION="${AWS_REGION:-ap-south-1}"
EMAIL="madhumitha19022@gmail.com"
PROJECT_TAG="AWS-Internship-Portal"

echo "=== [1/10] Creating Custom VPC (10.0.0.0/16) ==="
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=internship-vpc},{Key=Project,Value=$PROJECT_TAG}]" \
    --query 'Vpc.VpcId' --output text --region "$AWS_REGION")
echo "Created VPC: $VPC_ID"

aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames "{\"Value\":true}" --region "$AWS_REGION"
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-support "{\"Value\":true}" --region "$AWS_REGION"

echo "=== [2/10] Creating Public Subnet (10.0.1.0/24) ==="
SUBNET_ID=$(aws ec2 create-subnet \
    --vpc-id "$VPC_ID" \
    --cidr-block 10.0.1.0/24 \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=internship-public-subnet-1},{Key=Project,Value=$PROJECT_TAG}]" \
    --query 'Subnet.SubnetId' --output text --region "$AWS_REGION")
echo "Created Subnet: $SUBNET_ID"

# Enable Auto-Assign Public IP
aws ec2 modify-subnet-attribute --subnet-id "$SUBNET_ID" --map-public-ip-on-launch --region "$AWS_REGION"

echo "=== [3/10] Creating and Attaching Internet Gateway ==="
IGW_ID=$(aws ec2 create-internet-gateway \
    --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=internship-igw},{Key=Project,Value=$PROJECT_TAG}]" \
    --query 'InternetGateway.InternetGatewayId' --output text --region "$AWS_REGION")
echo "Created Internet Gateway: $IGW_ID"

aws ec2 attach-internet-gateway --vpc-id "$VPC_ID" --internet-gateway-id "$IGW_ID" --region "$AWS_REGION"

echo "=== [4/10] Creating Custom Route Table & Internet Route ==="
RTB_ID=$(aws ec2 create-route-table \
    --vpc-id "$VPC_ID" \
    --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=internship-public-rt},{Key=Project,Value=$PROJECT_TAG}]" \
    --query 'RouteTable.RouteTableId' --output text --region "$AWS_REGION")
echo "Created Route Table: $RTB_ID"

aws ec2 create-route --route-table-id "$RTB_ID" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW_ID" --region "$AWS_REGION"
aws ec2 associate-route-table --subnet-id "$SUBNET_ID" --route-table-id "$RTB_ID" --region "$AWS_REGION"

echo "=== [5/10] Creating Security Group (internship-web-sg) ==="
SG_ID=$(aws ec2 create-security-group \
    --group-name "internship-web-sg" \
    --description "Security group for AWS Internship Web Portal" \
    --vpc-id "$VPC_ID" \
    --query 'GroupId' --output text --region "$AWS_REGION")
echo "Created Security Group: $SG_ID"

# Inbound HTTP (Port 80)
aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp --port 80 --cidr 0.0.0.0/0 --region "$AWS_REGION"

# Inbound SSH (Port 22)
aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$AWS_REGION"

echo "=== [6/10] Creating S3 Storage Bucket with Block Public Access ==="
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="aws-internship-portal-madhumitha-$ACCOUNT_ID"

if [ "$AWS_REGION" == "us-east-1" ]; then
    aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$AWS_REGION"
else
    aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$AWS_REGION" \
        --create-bucket-configuration LocationConstraint="$AWS_REGION"
fi

aws s3api put-public-access-block \
    --bucket "$BUCKET_NAME" \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
echo "Created Private S3 Bucket: $BUCKET_NAME"

echo "=== [7/10] Creating Least-Privilege IAM Instance Role & Profile ==="
cat <<EOT > /tmp/ec2-trust-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOT

ROLE_NAME="EC2-Internship-Portal-Role"
aws iam create-role --role-name "$ROLE_NAME" --assume-role-policy-document file:///tmp/ec2-trust-policy.json || true

cat <<EOT > /tmp/s3-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::$BUCKET_NAME"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
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
EOT

aws iam put-role-policy --role-name "$ROLE_NAME" --policy-name "InternshipS3LeastPrivilegePolicy" --policy-document file:///tmp/s3-policy.json

PROFILE_NAME="EC2-Internship-Portal-Profile"
aws iam create-instance-profile --instance-profile-name "$PROFILE_NAME" || true
aws iam add-role-to-instance-profile --instance-profile-name "$PROFILE_NAME" --role-name "$ROLE_NAME" || true

echo "=== [8/10] Setting up SNS Topic & Email Alerts ==="
TOPIC_ARN=$(aws sns create-topic --name "internship-alerts-topic" --query 'TopicArn' --output text --region "$AWS_REGION")
aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$EMAIL" --region "$AWS_REGION"
echo "Subscribed $EMAIL to SNS Topic: $TOPIC_ARN"

echo "=== [9/10] Summary of Provisioned Network & Cloud Assets ==="
echo "VPC ID:           $VPC_ID"
echo "Subnet ID:        $SUBNET_ID"
echo "Security Group:   $SG_ID"
echo "S3 Bucket:        $BUCKET_NAME"
echo "IAM Profile:      $PROFILE_NAME"
echo "SNS Topic ARN:    $TOPIC_ARN"

echo "=== [10/10] Done! Ready to Launch EC2 Instance into $SUBNET_ID ==="
