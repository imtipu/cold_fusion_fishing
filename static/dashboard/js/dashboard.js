// function btnSidebarToggle() {
//     let btn = document.getElementById('btn-sidebar-toggle');
//     let sidebar = document.getElementById('nav-left-sidebar');
//     sidebar.classList.toggle('-translate-x-[280px]');
//
//     // if (sidebar.has('ml-[-280px]')) {
//     //     sidebar.classList.remove('ml-[-280px]');
//     // }
//     // evt.stopPropagation();
// }

$(document).on('click', '#btn-sidebar-toggle', function (evt) {
    evt.stopPropagation();
    let sidebar = document.getElementById('nav-left-sidebar');
    sidebar.classList.toggle('-translate-x-[280px]');
})

$(document).on('click', 'body', function (evt) {

    let sidebar = document.getElementById('nav-left-sidebar');

    if (evt.target !== sidebar) {
        // sidebar.classList.toggle('-translate-x-[280px]');
        if (!sidebar.classList.contains('-translate-x-[280px]')) {
            sidebar.classList.add('-translate-x-[280px]')
        }
    }
})


