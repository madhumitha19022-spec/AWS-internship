import os
import random
import datetime

os.makedirs('data', exist_ok=True)

ips = [
    '203.0.113.19', '198.51.100.45', '192.0.2.88', '198.51.100.12', '203.0.113.5',
    '192.0.2.14', '198.51.100.99', '203.0.113.82', '192.0.2.201', '198.51.100.67',
    '203.0.113.111', '192.0.2.45', '198.51.100.210', '203.0.113.33', '192.0.2.77',
    '198.51.100.150', '203.0.113.90', '192.0.2.16', '198.51.100.8', '203.0.113.44',
    '10.0.1.250', '10.0.1.251', '172.31.10.5'
]

paths = [
    ('/', 250, [200, 304]),
    ('/dashboard', 220, [200]),
    ('/project-info', 140, [200]),
    ('/log-analysis', 160, [200]),
    ('/aws-monitoring', 150, [200]),
    ('/about', 90, [200]),
    ('/health', 180, [200]),
    ('/api/aws/status', 130, [200]),
    ('/api/logs/summary', 110, [200]),
    ('/static/css/style.css', 150, [200, 304]),
    ('/static/js/main.js', 140, [200, 304]),
    ('/static/js/charts.js', 130, [200, 304]),
    ('/admin', 25, [401, 403]),
    ('/wp-login.php', 20, [404]),
    ('/api/v2/metrics', 18, [404]),
    ('/database.sql', 15, [403, 404]),
    ('/export-data', 16, [500, 502]),
    ('/api/s3/sync', 12, [500])
]

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Amazon-Route53-Health-Check-Service',
    'ELB-HealthChecker/2.0',
    'curl/8.5.0',
    'python-requests/2.31.0'
]

# Generate records distributed over a 24-hour period with peak around 14:00-16:00
base_date = datetime.datetime(2026, 11, 4, 0, 0, 0)
records = []

# Generate 750 realistic records
random.seed(42)
for i in range(750):
    hour_weights = [15, 10, 8, 5, 6, 12, 20, 35, 50, 65, 75, 80, 85, 95, 100, 90, 80, 70, 60, 55, 45, 35, 25, 20]
    hour = random.choices(range(24), weights=hour_weights)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    ts = base_date.replace(hour=hour, minute=minute, second=second).strftime('%Y-%m-%d %H:%M:%S')
    
    chosen_path_tuple = random.choices(paths, weights=[w for _, w, _ in paths])[0]
    path = chosen_path_tuple[0]
    status = random.choice(chosen_path_tuple[2])
    
    method = 'GET'
    if path in ['/export-data', '/api/s3/sync'] and random.random() > 0.4:
        method = 'POST'
    elif path == '/admin' and random.random() > 0.7:
        method = 'POST'
        
    ip = random.choice(ips)
    ua = random.choice(user_agents)
    
    if status == 200:
        bytes_sent = random.randint(1200, 48000)
    elif status in [301, 304]:
        bytes_sent = random.randint(150, 450)
    elif status in [401, 403, 404]:
        bytes_sent = random.randint(300, 1200)
    else:
        bytes_sent = random.randint(500, 1800)
        
    records.append((ts, ip, method, path, status, bytes_sent, ua))

records.sort(key=lambda r: r[0])

output_file = os.path.join('data', 'web-access-logs.csv')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('timestamp,ip,method,path,status,bytes,user_agent\n')
    for r in records:
        f.write(f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},\"{r[6]}\"\n')

print(f'Successfully generated {len(records)} log records in {output_file}')
