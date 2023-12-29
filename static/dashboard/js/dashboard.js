

function btnSidebarToggle() {
    let btn = document.getElementById('btn-sidebar-toggle');
    let sidebar = document.getElementById('nav-left-sidebar');
    sidebar.classList.toggle('-translate-x-[280px]');

    // if (sidebar.has('ml-[-280px]')) {
    //     sidebar.classList.remove('ml-[-280px]');
    // }
}
