"""
Unit Tests for Flask Web Application & Routes
=============================================
"""

import unittest
from app import app


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AWS Internship Portal', response.data)

    def test_dashboard_page_status(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cloud Operations &amp; Telemetry Dashboard', response.data)

    def test_project_info_page_status(self):
        response = self.client.get('/project-info')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Architecture, Design Specifications', response.data)

    def test_log_analysis_page_status(self):
        response = self.client.get('/log-analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Web Access Log Analytics', response.data)

    def test_aws_monitoring_page_status(self):
        response = self.client.get('/aws-monitoring')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Amazon CloudWatch, EC2 &amp; S3 Telemetry Center', response.data)

    def test_about_page_status(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Madhumitha A', response.data)

    def test_health_check_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'healthy')

    def test_api_logs_summary(self):
        response = self.client.get('/api/logs/summary')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('total_requests', json_data)
        self.assertIn('peak_traffic_hour', json_data)

    def test_api_aws_status(self):
        response = self.client.get('/api/aws/status')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('ec2', json_data)
        self.assertIn('cloudwatch', json_data)
        self.assertIn('s3', json_data)


if __name__ == '__main__':
    unittest.main()
