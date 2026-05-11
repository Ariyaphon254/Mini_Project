// ===== Sidebar Toggle =====
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');

if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (window.innerWidth > 768) {
            if (sidebar.style.width === '0px' || sidebar.style.width === '') {
                sidebar.style.width = '260px';
                mainContent.style.marginLeft = '260px';
            } else {
                sidebar.style.width = '0px';
                mainContent.style.marginLeft = '0';
            }
        }
    });
}

// ===== Auto-dismiss Flash Messages =====
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.flash-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 4000);
    });

    // ===== Add active class animation =====
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.classList.contains('active')) {
            item.style.animation = 'none';
        }
    });

    // ===== Stat Card Counter Animation =====
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(el => {
        const target = parseInt(el.textContent.replace(/,/g, '')) || 0;
        if (target > 0 && target < 10000) {
            let count = 0;
            const step = Math.ceil(target / 40);
            const timer = setInterval(() => {
                count += step;
                if (count >= target) {
                    el.textContent = target.toLocaleString();
                    clearInterval(timer);
                } else {
                    el.textContent = count.toLocaleString();
                }
            }, 25);
        }
    });

    // ===== Table Row Hover Effect =====
    document.querySelectorAll('tbody tr').forEach(row => {
        row.style.transition = 'background 0.15s ease';
    });
});

// ===== Confirm Delete =====
function confirmDelete(name) {
    return confirm(`คุณต้องการลบ "${name}" ใช่หรือไม่?\nการดำเนินการนี้ไม่สามารถย้อนกลับได้`);
}

// ===== Tooltip Init =====
document.addEventListener('DOMContentLoaded', () => {
    const tooltips = document.querySelectorAll('[title]');
    tooltips.forEach(el => {
        new bootstrap.Tooltip(el, { trigger: 'hover', placement: 'top' });
    });
});

// ===== Current Date for Navbar =====
document.addEventListener('DOMContentLoaded', () => {
    const dateEl = document.querySelector('.navbar-right .text-muted.small');
    if (dateEl && !dateEl.textContent.trim()) {
        const now = new Date();
        const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
        dateEl.textContent = now.toLocaleDateString('th-TH', options);
    }
});
