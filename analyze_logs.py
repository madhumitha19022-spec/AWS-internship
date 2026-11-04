#!/usr/bin/env python3
"""
AWS Cloud Internship Project: Web Access Log Analyzer
=====================================================
Analyzes web server access logs (CSV format) to extract critical performance metrics,
traffic distributions, HTTP response codes, and security error rates.
Integrates directly with the Student Internship Portal dashboard.
"""

import os
import csv
import sys
import json
from collections import Counter, defaultdict
from datetime import datetime

DEFAULT_LOG_PATH = os.path.join(os.path.dirname(__file__), 'data', 'web-access-logs.csv')


def parse_logs(file_path=DEFAULT_LOG_PATH):
    """
    Parses web access logs from CSV.
    Expected columns: timestamp, ip, method, path, status, bytes, user_agent
    """
    records = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Log file not found at: {file_path}")

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = {
                    'timestamp': row['timestamp'].strip(),
                    'ip': row['ip'].strip(),
                    'method': row['method'].strip().upper(),
                    'path': row['path'].strip(),
                    'status': int(row['status']),
                    'bytes': int(row.get('bytes', 0)),
                    'user_agent': row.get('user_agent', '').strip()
                }
                records.append(record)
            except (ValueError, KeyError):
                continue
    return records


def analyze_log_records(records):
    """
    Performs comprehensive statistical and behavioral log analysis.
    """
    total_requests = len(records)
    if total_requests == 0:
        return {
            'total_requests': 0,
            'unique_ips_count': 0,
            'successful_requests': 0,
            'errors_4xx': 0,
            'errors_5xx': 0,
            'peak_traffic_hour': 'N/A',
            'top_pages': [],
            'status_distribution': {},
            'hourly_distribution': {},
            'method_distribution': {},
            'top_ips': [],
            'is_sample_data': True
        }

    ip_counter = Counter()
    path_counter = Counter()
    status_counter = Counter()
    method_counter = Counter()
    hourly_counter = defaultdict(int)

    successful_requests = 0
    errors_4xx = 0
    errors_5xx = 0
    total_bytes = 0

    for r in records:
        ip_counter[r['ip']] += 1
        path_counter[r['path']] += 1
        status = r['status']
        status_counter[status] += 1
        method_counter[r['method']] += 1
        total_bytes += r['bytes']

        # Categorize status
        if 200 <= status < 400:
            successful_requests += 1
        elif 400 <= status < 500:
            errors_4xx += 1
        elif 500 <= status < 600:
            errors_5xx += 1

        # Extract hour from timestamp
        try:
            dt = datetime.strptime(r['timestamp'], '%Y-%m-%d %H:%M:%S')
            hour_str = f"{dt.hour:02d}:00"
            hourly_counter[hour_str] += 1
        except ValueError:
            pass

    # Determine peak traffic hour
    peak_hour, peak_count = 'N/A', 0
    if hourly_counter:
        peak_hour, peak_count = max(hourly_counter.items(), key=lambda item: item[1])

    # Top requested pages (top 10)
    top_pages = [
        {'path': path, 'count': count, 'percentage': round((count / total_requests) * 100, 2)}
        for path, count in path_counter.most_common(10)
    ]

    # Top visitor IPs (top 10)
    top_ips = [
        {'ip': ip, 'count': count, 'percentage': round((count / total_requests) * 100, 2)}
        for ip, count in ip_counter.most_common(10)
    ]

    # Hourly distribution formatted sorted chronologically (00:00 to 23:00)
    sorted_hourly = []
    for h in range(24):
        h_str = f"{h:02d}:00"
        sorted_hourly.append({
            'hour': h_str,
            'count': hourly_counter.get(h_str, 0)
        })

    # Status distribution
    status_distribution = {str(k): v for k, v in sorted(status_counter.items())}

    return {
        'total_requests': total_requests,
        'unique_ips_count': len(ip_counter),
        'successful_requests': successful_requests,
        'success_rate': round((successful_requests / total_requests) * 100, 2),
        'errors_4xx': errors_4xx,
        'errors_5xx': errors_5xx,
        'error_rate': round(((errors_4xx + errors_5xx) / total_requests) * 100, 2),
        'total_bandwidth_mb': round(total_bytes / (1024 * 1024), 2),
        'peak_traffic_hour': peak_hour,
        'peak_traffic_count': peak_count,
        'top_pages': top_pages,
        'top_ips': top_ips,
        'status_distribution': status_distribution,
        'hourly_distribution': sorted_hourly,
        'method_distribution': dict(method_counter),
        'is_sample_data': True,
        'dataset_source': 'Simulated AWS Access Logs (data/web-access-logs.csv)'
    }


def get_log_analytics(file_path=DEFAULT_LOG_PATH):
    """Convenience helper for Flask backend and API endpoints."""
    records = parse_logs(file_path)
    return analyze_log_records(records)


def print_cli_report(metrics):
    """Prints a clean, professional terminal report."""
    border = "=" * 70
    sub_border = "-" * 70

    print("\n" + border)
    print("      AWS CLOUD INTERNSHIP: WEB ACCESS LOG ANALYSIS REPORT")
    print("        [Sample Dataset: data/web-access-logs.csv]")
    print(border)
    print(f"Total Requests Analyzed:      {metrics['total_requests']:,}")
    print(f"Unique Visitor IPs:           {metrics['unique_ips_count']:,}")
    print(f"Successful Requests (2xx/3xx): {metrics['successful_requests']:,} ({metrics['success_rate']}%)")
    print(f"Client Errors (4xx):          {metrics['errors_4xx']:,}")
    print(f"Server Errors (5xx):          {metrics['errors_5xx']:,}")
    print(f"Overall Error Rate:           {metrics['error_rate']}%")
    print(f"Peak Traffic Hour:            {metrics['peak_traffic_hour']} ({metrics['peak_traffic_count']} requests)")
    print(f"Total Bandwidth Transferred:  {metrics['total_bandwidth_mb']} MB")
    print(sub_border)

    print("\nTOP REQUESTED PAGES:")
    print(f"{'Page / Path':<35} {'Requests':<12} {'Percentage':<10}")
    print("-" * 60)
    for p in metrics['top_pages'][:8]:
        print(f"{p['path']:<35} {p['count']:<12} {p['percentage']:>6.2f}%")

    print("\nHTTP STATUS CODE DISTRIBUTION:")
    for status, count in metrics['status_distribution'].items():
        pct = (count / metrics['total_requests']) * 100
        print(f"  Status {status}: {count:>4} requests ({pct:>5.1f}%)")

    print("\nHTTP METHODS BREAKDOWN:")
    for method, count in metrics['method_distribution'].items():
        print(f"  {method:<6}: {count} requests")

    print("\nTOP 5 VISITOR IP ADDRESSES:")
    for ip_info in metrics['top_ips'][:5]:
        print(f"  {ip_info['ip']:<20} {ip_info['count']:>4} requests ({ip_info['percentage']}%)")

    print(border + "\n")


if __name__ == '__main__':
    log_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOG_PATH
    try:
        results = get_log_analytics(log_file)
        print_cli_report(results)
    except Exception as e:
        print(f"Error during log analysis: {e}", file=sys.stderr)
        sys.exit(1)
