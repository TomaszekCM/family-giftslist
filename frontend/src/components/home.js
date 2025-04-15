import $ from 'jquery';

// function to show hidden gift data
$('#gift-list').on('click', '.toggle-details', function(e) {
    e.preventDefault();
    $(this).next('.gift-details').slideToggle();
});


$(document).ready(function() {
    const modal = $('#add-gift-modal');
    const btn = $('#add-gift-button');

    // this shows form
    btn.click(function() {
        modal.css('display', 'block');
    });

    // this closes window once user click x
    $('.close').click(function() {
        modal.css('display', 'none');
    });

    // this closes window once user clicks outside the form window
    $(window).click(function(event) {
        if (event.target === modal[0]) {
            modal.css('display', 'none');
        }
    });

    // and finally once user submit the form
    $('#add-gift-form').submit(function(event) {
        const url = document.getElementById("add-gift-button").dataset.url;
        event.preventDefault();

        $.ajax({
            url: url,
            type: 'POST',
            data: $(this).serialize(),
            success: function(data) {
                $('#gift-list').append(data);
                $('#add-gift-form')[0].reset();
                modal.css('display', 'none');
            },
            error: function(xhr) {
                const response = JSON.parse(xhr.responseText);

                if (response.errors) {
                    let errorMessage = '';
                    for (let field in response.errors) {
                        if (response.errors[field].length) {
                            errorMessage = response.errors[field][0];
                            break;
                        }
                    }
                    alert(errorMessage || "Wystąpił nieznany błąd.");
                } else {
                    alert("Wystąpił nieoczekiwany błąd.");
                }
            }
        });
    });
});

// SORTING GIFTS LIST
document.addEventListener('DOMContentLoaded', function () {
    const sortSelect = document.getElementById('sort-gifts');
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


// HIDE/SHOW MENU
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.toggle-sidebar');
    const sidebar = document.getElementById('sidebar');

    toggleBtn?.addEventListener('click', function (e) {
      e.preventDefault();
      sidebar.classList.toggle('show');
    });
});
