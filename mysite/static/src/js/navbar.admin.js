window.addEventListener('DOMContentLoaded', async function () {
    const menuButton = document.getElementById('menu-button');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    function openSidebar() {
        sidebar.classList.add('translate-x-0');
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
    }

    // Function to close the sidebar
    function closeSidebar() {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
        overlay.classList.add('hidden');
    }
    overlay.addEventListener('click', () => {
        console.log("holaaa")
        closeSidebar();
    });

    menuButton.addEventListener('click', () => {
        if (sidebar.classList.contains('-translate-x-full')) {
            openSidebar();
        } else {
            closeSidebar();
        }
    });
})