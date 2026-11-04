"""
Unit Tests for Log Analyzer Engine
==================================
"""

import unittest
import os
from analyze_logs import parse_logs, analyze_log_records, DEFAULT_LOG_PATH


class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.sample_records = [
            {'timestamp': '2026-11-04 14:10:00', 'ip': '203.0.113.1', 'method': 'GET', 'path': '/', 'status': 200, 'bytes': 1500, 'user_agent': 'Mozilla/5.0'},
            {'timestamp': '2026-11-04 14:15:00', 'ip': '203.0.113.2', 'method': 'GET', 'path': '/dashboard', 'status': 200, 'bytes': 2500, 'user_agent': 'Mozilla/5.0'},
            {'timestamp': '2026-11-04 14:20:00', 'ip': '203.0.113.1', 'method': 'GET', 'path': '/unknown', 'status': 404, 'bytes': 450, 'user_agent': 'curl/8.0'},
            {'timestamp': '2026-11-04 15:00:00', 'ip': '203.0.113.3', 'method': 'POST', 'path': '/api/fail', 'status': 500, 'bytes': 600, 'user_agent': 'python-requests'},
            {'timestamp': '2026-11-04 15:30:00', 'ip': '203.0.113.4', 'method': 'GET', 'path': '/static/css/style.css', 'status': 304, 'bytes': 120, 'user_agent': 'Mozilla/5.0'},
        ]

    def test_analyze_records_calculation(self):
        metrics = analyze_log_records(self.sample_records)
        self.assertEqual(metrics['total_requests'], 5)
        self.assertEqual(metrics['unique_ips_count'], 4)
        self.assertEqual(metrics['successful_requests'], 3)  # 200, 200, 304
        self.assertEqual(metrics['errors_4xx'], 1)  # 404
        self.assertEqual(metrics['errors_5xx'], 1)  # 500
        self.assertEqual(metrics['peak_traffic_hour'], '14:00')
        self.assertEqual(metrics['peak_traffic_count'], 3)

    def test_actual_csv_file_parsing(self):
        if os.path.exists(DEFAULT_LOG_PATH):
            records = parse_logs(DEFAULT_LOG_PATH)
            self.assertGreaterEqual(len(records), 200)
            metrics = analyze_log_records(records)
            self.assertIn('total_requests', metrics)
            self.assertIn('peak_traffic_hour', metrics)
            self.assertIn('top_pages', metrics)


if __name__ == '__main__':
    unittest.main()
