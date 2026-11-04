#!/bin/bash
# =============================================================================
# AWS Cloud Internship Project: EBS Automated Snapshot Backup
# =============================================================================
# Usage:
#   bash infra/backup_snapshot.sh [INSTANCE_ID]
# If INSTANCE_ID is omitted, it will automatically query the EC2 metadata service.
# =============================================================================

set -e

AWS_REGION="${AWS_REGION:-ap-south-1}"

# Determine Instance ID
INSTANCE_ID="$1"
if [ -z "$INSTANCE_ID" ]; then
    echo "Querying EC2 Metadata Service for local Instance ID..."
    INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id || true)
fi

if [ -z "$INSTANCE_ID" ]; then
    echo "ERROR: Please provide an Instance ID: bash infra/backup_snapshot.sh i-0123456789abcdef0"
    exit 1
fi

echo "Retrieving Root EBS Volume ID for instance: $INSTANCE_ID..."
VOLUME_ID=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$AWS_REGION" \
    --query "Reservations[0].Instances[0].BlockDeviceMappings[?DeviceName=='/dev/sda1' || DeviceName=='/dev/xvda'].Ebs.VolumeId" \
    --output text)

if [ -z "$VOLUME_ID" ] || [ "$VOLUME_ID" == "None" ]; then
    echo "ERROR: Could not locate root volume attached to $INSTANCE_ID"
    exit 1
fi

TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
SNAPSHOT_DESC="Internship Portal Root Backup - $TIMESTAMP"

echo "Creating Point-in-Time Snapshot for Volume $VOLUME_ID..."
SNAPSHOT_ID=$(aws ec2 create-snapshot \
    --volume-id "$VOLUME_ID" \
    --description "$SNAPSHOT_DESC" \
    --region "$AWS_REGION" \
    --tag-specifications "ResourceType=snapshot,Tags=[{Key=Name,Value=Internship-Portal-Root-Backup},{Key=Project,Value=AWS-Internship-Portal},{Key=Created,Value=$TIMESTAMP}]" \
    --query "SnapshotId" \
    --output text)

echo "============================================================================="
echo " SNAPSHOT CREATION INITIATED"
echo " Snapshot ID:  $SNAPSHOT_ID"
echo " Volume ID:    $VOLUME_ID"
echo " Region:       $AWS_REGION"
echo " Description:  $SNAPSHOT_DESC"
echo "============================================================================="
echo "To verify snapshot status, run:"
echo "  aws ec2 describe-snapshots --snapshot-ids $SNAPSHOT_ID --region $AWS_REGION"
