"""
Log Service Module
==================
Integrates log parsing and statistical analytics with Flask views.
"""

import os
from analyze_logs import parse_logs, analyze_log_records
from config import Config


class LogService:
    @staticmethod
    def get_summary(file_path=None):
        path = file_path or Config.LOG_DATA_PATH
        records = parse_logs(path)
        return analyze_log_records(records)

    @staticmethod
    def get_raw_logs(file_path=None, limit=100, status_filter=None, method_filter=None):
        path = file_path or Config.LOG_DATA_PATH
        records = parse_logs(path)

        filtered = []
        for r in records:
            if status_filter:
                if status_filter == '4xx' and not (400 <= r['status'] < 500):
                    continue
                elif status_filter == '5xx' and not (500 <= r['status'] < 600):
                    continue
                elif status_filter == '2xx' and not (200 <= r['status'] < 300):
                    continue
                elif status_filter.isdigit() and r['status'] != int(status_filter):
                    continue

            if method_filter and r['method'] != method_filter.upper():
                continue

            filtered.append(r)

        # Return latest entries up to limit
        return filtered[-limit:]
