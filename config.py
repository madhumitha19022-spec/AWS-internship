"""
AWS Cloud Internship Project - Application Configuration
=========================================================
Manages environment variables, AWS settings, and application constants.
Enforces security: no secrets or credentials are hardcoded.
"""

import os
from dotenv import load_dotenv

# Load optional .env file for local development
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'cloud-internship-secure-session-key-2026')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

    # AWS Configuration
    # AWS Region defaults to ap-south-1 (Mumbai) or us-east-1
    AWS_REGION = os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'ap-south-1'))
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'aws-internship-portal-madhumitha')
    SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN', '')

    # Log analytics data path
    LOG_DATA_PATH = os.getenv('LOG_DATA_PATH', os.path.join(BASE_DIR, 'data', 'web-access-logs.csv'))

    # Project metadata
    PROJECT_TITLE = "AWS Cloud Internship: Student Internship Portal & Infrastructure"
    PROJECT_VERSION = "1.0.0"
    DEVELOPER_NAME = "Madhumitha A"
    DEVELOPER_EMAIL = "madhumitha19022@gmail.com"
    GITHUB_REPO = "https://github.com/madhumitha19022-spec/AWS-internship"
