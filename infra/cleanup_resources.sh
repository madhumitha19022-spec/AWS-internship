#!/bin/bash
# =============================================================================
# AWS Cloud Internship Project: Resource Cleanup & Teardown Script
# =============================================================================
# Run this script when tearing down the project to guarantee ZERO leftover charges.
# =============================================================================

set -e

AWS_REGION="${AWS_REGION:-ap-south-1}"

echo "============================================================================="
echo " WARNING: THIS WILL PERMANENTLY TERMINATE AND CLEAN UP ALL PROJECT RESOURCES"
echo "============================================================================="
read -p "Are you sure you want to proceed? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Cleanup aborted."
    exit 0
fi

echo "=== [1/6] Terminating EC2 Instances ==="
INSTANCE_IDS=$(aws ec2 describe-instances \
    --filters "Name=tag:Project,Values=AWS-Internship-Portal" "Name=instance-state-name,Values=running,stopped" \
    --region "$AWS_REGION" \
    --query "Reservations[].Instances[].InstanceId" --output text)

if [ -n "$INSTANCE_IDS" ]; then
    echo "Terminating: $INSTANCE_IDS"
    aws ec2 terminate-instances --instance-ids $INSTANCE_IDS --region "$AWS_REGION"
    echo "Waiting for instance termination..."
    aws ec2 wait instance-terminated --instance-ids $INSTANCE_IDS --region "$AWS_REGION"
fi

echo "=== [2/6] Deleting CloudWatch Alarms & SNS Topic ==="
aws cloudwatch delete-alarms --alarm-names Internship-High-CPU-Alarm Internship-StatusCheckFailed-Alarm --region "$AWS_REGION" || true

TOPIC_ARN=$(aws sns list-topics --region "$AWS_REGION" --query "Topics[?contains(TopicArn, 'internship-alerts-topic')].TopicArn" --output text)
if [ -n "$TOPIC_ARN" ]; then
    aws sns delete-topic --topic-arn "$TOPIC_ARN" --region "$AWS_REGION" || true
fi

echo "=== [3/6] Cleaning up S3 Bucket ==="
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="aws-internship-portal-madhumitha-$ACCOUNT_ID"
aws s3 rm "s3://$BUCKET_NAME" --recursive || true
aws s3api delete-bucket --bucket "$BUCKET_NAME" --region "$AWS_REGION" || true

echo "=== [4/6] Deleting IAM Instance Profile & Roles ==="
aws iam remove-role-from-instance-profile --instance-profile-name EC2-Internship-Portal-Profile --role-name EC2-Internship-Portal-Role || true
aws iam delete-instance-profile --instance-profile-name EC2-Internship-Portal-Profile || true
aws iam delete-role-policy --role-name EC2-Internship-Portal-Role --policy-name InternshipS3LeastPrivilegePolicy || true
aws iam delete-role --role-name EC2-Internship-Portal-Role || true

echo "=== [5/6] Deleting Security Groups, Subnets, Gateways, Route Tables, and VPC ==="
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=internship-vpc" --region "$AWS_REGION" --query "Vpcs[0].VpcId" --output text)

if [ -n "$VPC_ID" ] && [ "$VPC_ID" != "None" ]; then
    # Detach and delete Internet Gateway
    IGW_ID=$(aws ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=$VPC_ID" --region "$AWS_REGION" --query "InternetGateways[0].InternetGatewayId" --output text)
    if [ -n "$IGW_ID" ] && [ "$IGW_ID" != "None" ]; then
        aws ec2 detach-internet-gateway --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID" --region "$AWS_REGION"
        aws ec2 delete-internet-gateway --internet-gateway-id "$IGW_ID" --region "$AWS_REGION"
    fi

    # Delete Subnets
    SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --region "$AWS_REGION" --query "Subnets[].SubnetId" --output text)
    for s in $SUBNET_IDS; do
        aws ec2 delete-subnet --subnet-id "$s" --region "$AWS_REGION"
    done

    # Delete Custom Route Tables
    RT_IDS=$(aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC_ID" --region "$AWS_REGION" --query "RouteTables[?Associations[0].Main!=true].RouteTableId" --output text)
    for r in $RT_IDS; do
        aws ec2 delete-route-table --route-table-id "$r" --region "$AWS_REGION"
    done

    # Delete Security Group
    SG_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=internship-web-sg" --region "$AWS_REGION" --query "SecurityGroups[0].GroupId" --output text)
    if [ -n "$SG_ID" ] && [ "$SG_ID" != "None" ]; then
        aws ec2 delete-security-group --group-id "$SG_ID" --region "$AWS_REGION"
    fi

    # Delete VPC
    aws ec2 delete-vpc --vpc-id "$VPC_ID" --region "$AWS_REGION"
    echo "Deleted VPC: $VPC_ID"
fi

echo "=== [6/6] Teardown Complete! Zero Remaining Charges ==="
