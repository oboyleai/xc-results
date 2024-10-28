// Dark mode toggle
document.getElementById('darkModeToggle').addEventListener('click', () => {
    document.body.dataset.theme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
});

// Expandable sections
document.querySelectorAll('.expandable').forEach(section => {
    const btn = section.querySelector('.expand-btn');
    btn.addEventListener('click', () => {
        section.classList.toggle('expanded');
    });
});