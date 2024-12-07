// Sidebar toggle function
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    sidebar.classList.toggle('open');
    mainContent.classList.toggle('open');
}

// Submenu toggle function
function toggleSubmenu() {
    const submenu = document.querySelector('.sidebar .submenu');
    submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
}
