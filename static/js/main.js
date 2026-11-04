/**
 * AWS Cloud Internship Portal - Main Client JS
 */

document.addEventListener('DOMContentLoaded', function () {
    // Live Clock display if present
    const clockElement = document.getElementById('utc-clock');
    if (clockElement) {
        function updateClock() {
            const now = new Date();
            clockElement.textContent = now.toUTCString().replace('GMT', 'UTC');
        }
        updateClock();
        setInterval(updateClock, 1000);
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
