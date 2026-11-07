"""
AWS Cloud Internship Project: Student Internship Portal
======================================================
Full-Stack Flask Web Application hosted on AWS EC2 inside a Custom VPC,
integrated with Amazon S3, IAM Roles, CloudWatch, SNS, and Log Analysis.

Author: Madhumitha A
Repository: https://github.com/madhumitha19022-spec/AWS-internship
"""

import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from config import Config
from services.log_service import LogService
from services.aws_service import aws_service

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config.from_object(Config)


@app.context_processor
def inject_global_context():
    """Injects common project metadata and live AWS status across all templates."""
    return {
        'project_title': Config.PROJECT_TITLE,
        'developer_name': Config.DEVELOPER_NAME,
        'github_repo': Config.GITHUB_REPO,
        'aws_region': Config.AWS_REGION,
        'is_live_aws': aws_service.is_live_aws(),
        's3_bucket': Config.S3_BUCKET_NAME
    }


# -----------------------------------------------------------------------------
# Web Page Routes
# -----------------------------------------------------------------------------

@app.route('/')
def home():
    """Home Page: Hero, project overview, AWS services grid, and internship objectives."""
    ec2_info = aws_service.get_ec2_instance_metadata()
    log_summary = LogService.get_summary()
    return render_template(
        'index.html',
        ec2=ec2_info,
        log_summary=log_summary,
        active_page='home'
    )


@app.route('/dashboard')
def dashboard():
    """Dashboard: KPI metrics, server status, S3 storage overview, and recent activity."""
    log_summary = LogService.get_summary()
    ec2_info = aws_service.get_ec2_instance_metadata()
    cw_metrics = aws_service.get_cloudwatch_metrics()
    s3_info = aws_service.get_s3_storage_info()
    recent_logs = LogService.get_raw_logs(limit=10)

    return render_template(
        'dashboard.html',
        summary=log_summary,
        ec2=ec2_info,
        cw=cw_metrics,
        s3=s3_info,
        recent_logs=recent_logs,
        active_page='dashboard'
    )


@app.route('/project-info')
def project_info():
    """Project Information: System architecture, AWS services breakdown, implementation workflow."""
    return render_template('project_info.html', active_page='project_info')


@app.route('/log-analysis')
def log_analysis():
    """Log Analysis Page: Visual traffic breakdown, error drilldown, top endpoints, and raw data table."""
    status_filter = request.args.get('status', None)
    method_filter = request.args.get('method', None)

    summary = LogService.get_summary()
    logs = LogService.get_raw_logs(limit=50, status_filter=status_filter, method_filter=method_filter)

    return render_template(
        'log_analysis.html',
        summary=summary,
        logs=logs,
        selected_status=status_filter,
        selected_method=method_filter,
        active_page='log_analysis'
    )


@app.route('/aws-monitoring')
def aws_monitoring():
    """AWS Monitoring Page: EC2 health, CloudWatch alarms, CPU utilization graph, S3 explorer."""
    ec2_info = aws_service.get_ec2_instance_metadata()
    cw_info = aws_service.get_cloudwatch_metrics()
    s3_info = aws_service.get_s3_storage_info()

    return render_template(
        'aws_monitoring.html',
        ec2=ec2_info,
        cw=cw_info,
        s3=s3_info,
        active_page='aws_monitoring'
    )


@app.route('/about')
def about():
    """About Page: Developer profile, internship details, technologies, and certifications."""
    return render_template('about.html', active_page='about')


# -----------------------------------------------------------------------------
# REST API Endpoints
# -----------------------------------------------------------------------------

@app.route('/health')
def health():
    """Application health check endpoint for EC2 / ELB monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'student-internship-portal',
        'version': Config.PROJECT_VERSION,
        'environment': 'AWS EC2' if aws_service.is_live_aws() else 'Local / Simulation'
    }), 200


@app.route('/api/logs/summary')
def api_logs_summary():
    """JSON API endpoint returning computed log statistics."""
    summary = LogService.get_summary()
    return jsonify(summary)


@app.route('/api/aws/status')
def api_aws_status():
    """JSON API endpoint returning real-time AWS health and telemetry."""
    return jsonify({
        'ec2': aws_service.get_ec2_instance_metadata(),
        'cloudwatch': aws_service.get_cloudwatch_metrics(),
        's3': aws_service.get_s3_storage_info()
    })


@app.route('/api/s3/upload', methods=['POST'])
def api_s3_upload():
    """Endpoint to test S3 object upload via IAM instance profile."""
    file_name = request.form.get('file_name', 'test_upload.txt').strip()
    content = request.form.get('file_content', 'AWS Internship Portal Test Payload')
    result = aws_service.upload_test_file_to_s3(content, file_name)
    flash(result['message'], 'success' if result['success'] else 'danger')
    return redirect(url_for('aws_monitoring'))


# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    print(f"Starting {Config.PROJECT_TITLE}")
    print(f"Environment: {'Live AWS' if aws_service.is_live_aws() else 'Demonstration/Simulation'}")
    print(f"Server running at: http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
