// HIDE/SHOW MENU
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.toggle-sidebar');
    const sidebar = document.getElementById('sidebar');

    toggleBtn?.addEventListener('click', function (e) {
      e.preventDefault();
      sidebar.classList.toggle('show');
    });
});
