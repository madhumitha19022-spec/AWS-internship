/**
 * Chart.js Visualizations for Log Analytics and CloudWatch Metrics
 */

function initLogCharts(summaryData) {
    if (!summaryData) return;

    // 1. Hourly Traffic Distribution (Peak hours)
    const hourlyCtx = document.getElementById('hourlyTrafficChart');
    if (hourlyCtx && summaryData.hourly_distribution) {
        const labels = summaryData.hourly_distribution.map(d => d.hour);
        const counts = summaryData.hourly_distribution.map(d => d.count);

        new Chart(hourlyCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Requests / Hour',
                    data: counts,
                    fill: true,
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    borderColor: '#0D6EFD',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#00D2D3',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    tension: 0.35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#0A192F',
                        titleColor: '#00D2D3',
                        bodyColor: '#FFFFFF',
                        padding: 10,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        grid: { display: false }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0,0,0,0.05)' }
                    }
                }
            }
        });
    }

    // 2. HTTP Status Codes Donut Chart
    const statusCtx = document.getElementById('statusCodesChart');
    if (statusCtx && summaryData.status_distribution) {
        const labels = Object.keys(summaryData.status_distribution).map(k => `Status ${k}`);
        const counts = Object.values(summaryData.status_distribution);

        // Color mapping for status codes
        const statusColors = {
            'Status 200': '#10B981', // Success green
            'Status 301': '#3B82F6', // Blue redirect
            'Status 304': '#06B6D4', // Cyan cached
            'Status 401': '#F59E0B', // Amber auth error
            'Status 403': '#EA580C', // Orange forbidden
            'Status 404': '#EF4444', // Red not found
            'Status 500': '#DC2626', // Dark red server error
            'Status 502': '#991B1B'  // Bad gateway
        };

        const bgColors = labels.map(l => statusColors[l] || '#64748B');

        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: bgColors,
                    borderWidth: 2,
                    borderColor: '#FFFFFF'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            padding: 14,
                            font: { size: 11 }
                        }
                    }
                },
                cutout: '68%'
            }
        });
    }

    // 3. Top Visited Endpoints Bar Chart
    const endpointsCtx = document.getElementById('topEndpointsChart');
    if (endpointsCtx && summaryData.top_pages) {
        const pages = summaryData.top_pages.slice(0, 6);
        const labels = pages.map(p => p.path);
        const counts = pages.map(p => p.count);

        new Chart(endpointsCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Hits',
                    data: counts,
                    backgroundColor: 'rgba(13, 110, 253, 0.85)',
                    hoverBackgroundColor: '#0D6EFD',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0,0,0,0.05)' }
                    },
                    y: {
                        grid: { display: false }
                    }
                }
            }
        });
    }
}

function initCpuChart(cpuHistory) {
    const cpuCtx = document.getElementById('cpuUtilizationChart');
    if (!cpuCtx || !cpuHistory) return;

    const labels = cpuHistory.map(d => d.time);
    const data = cpuHistory.map(d => d.cpu);

    new Chart(cpuCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'CPU Utilization (%)',
                data: data,
                fill: true,
                backgroundColor: 'rgba(0, 210, 211, 0.12)',
                borderColor: '#00D2D3',
                borderWidth: 2.5,
                pointBackgroundColor: '#0A192F',
                pointBorderColor: '#00D2D3',
                pointRadius: 4,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: val => val + '%'
                    }
                }
            }
        }
    });
}
