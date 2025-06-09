import $ from 'jquery';

// SORTING GIFTS LIST
document.addEventListener('DOMContentLoaded', function () {
    const sortSelect = document.getElementById('sort-gifts');
    // If we are not on the gifts list page, do not execute the code
    if (!sortSelect) return;

    const sortToggle = document.getElementById('toggle-sort-direction');
    const giftList = document.getElementById('gift-list');

    let sortAscending = true;

    function sortGifts() {
        const sortBy = sortSelect.value;
        const gifts = Array.from(giftList.querySelectorAll('.gift-preview'));

        gifts.sort((a, b) => {
            const aVal = a.dataset[sortBy] || '';
            const bVal = b.dataset[sortBy] || '';

            let comparison;
            if (sortBy === 'price') {
                comparison = parseFloat(aVal) - parseFloat(bVal);
            } else if (sortBy === 'date') {
                comparison = new Date(aVal) - new Date(bVal);
            } else {
                comparison = aVal.localeCompare(bVal);
            }

            return sortAscending ? comparison : -comparison;
        });

        gifts.forEach(g => giftList.appendChild(g));
    }

    sortSelect.addEventListener('change', sortGifts);
    sortToggle.addEventListener('click', () => {
        sortAscending = !sortAscending;
        sortToggle.textContent = sortAscending ? '↑' : '↓';
        sortGifts();
    });
});