import $ from 'jquery';

// FILTERING GIFTSLIST
document.addEventListener('DOMContentLoaded', function () {
    const toggleFiltersBtn = document.getElementById('toggle-filters');
    const filtersSection = document.getElementById('filters-section');
    const giftList = document.getElementById('gift-list');

    const nameInput = document.getElementById('filter-name');
    const categorySelect = document.getElementById('filter-category');
    const minPriceInput = document.getElementById('filter-min-price');
    const maxPriceInput = document.getElementById('filter-max-price');

    toggleFiltersBtn.addEventListener('click', () => {
        filtersSection.style.display = filtersSection.style.display === 'none' ? 'block' : 'none';
    });


    function filterGifts() {
        const name = nameInput.value.toLowerCase();
        const category = categorySelect.value;
        const minPrice = parseFloat(minPriceInput.value) || 0;
        const maxPrice = parseFloat(maxPriceInput.value) || Infinity;
        const gifts = giftList.querySelectorAll('.gift-preview');

        let visibleCount = 0;

        gifts.forEach(gift => {
            const giftName = gift.dataset.name.toLowerCase();
            const giftCategory = gift.dataset.category;
            const giftPrice = parseFloat(gift.dataset.price);

            const matchesName = giftName.includes(name);
            const matchesCategory = !category || giftCategory === category;
            const matchesPrice = giftPrice >= minPrice && giftPrice <= maxPrice;

            const visible = matchesName && matchesCategory && matchesPrice;
            gift.style.display = visible ? '' : 'none';

            if (visible) visibleCount++;
        });

        const countElem = document.getElementById('filter-count');
        countElem.textContent = `Wyświetlono ${visibleCount} z ${gifts.length} prezentów`;
    }

    const clearBtn = document.getElementById('clear-filters');

    clearBtn.addEventListener('click', () => {
        nameInput.value = '';
        categorySelect.value = '';
        minPriceInput.value = '';
        maxPriceInput.value = '';
        filterGifts();
    });

    [nameInput, categorySelect, minPriceInput, maxPriceInput].forEach(input =>
        input.addEventListener('input', filterGifts)
    );
});