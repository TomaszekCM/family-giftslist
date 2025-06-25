export class UserList {
    constructor() {
        console.log('UserList constructor called');
        this.table = document.querySelector('table');
        if (!this.table) {
            console.log('No table found on the page');
            return;
        }
        console.log('Table found, setting up...');

        this.setupSorting();
        this.setupClickableRows();
    }

    setupSorting() {
        const headers = this.table.querySelectorAll('th a');
        headers.forEach(header => {
            header.addEventListener('click', (e) => {
                e.preventDefault();
                this.sortTable(header);
            });
        });
    }

    setupClickableRows() {
        console.log('Setting up clickable rows...');
        const rows = this.table.querySelectorAll('.clickable-row');
        console.log('Found clickable rows:', rows.length);
        
        rows.forEach(row => {
            console.log('Adding click handler to row with href:', row.dataset.href);
            row.addEventListener('click', function(e) {
                console.log('Row clicked, href:', this.dataset.href);
                window.location.href = this.dataset.href;
            });
        });
    }

    sortTable(header) {
        const column = header.textContent.trim();
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const currentDirection = header.getAttribute('data-direction') || 'asc';
        const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
        
        // Update sort direction
        header.setAttribute('data-direction', newDirection);
        
        // Update sort icon
        const icon = header.querySelector('i');
        if (icon) {
            icon.className = newDirection === 'asc' ? 'bi bi-arrow-down-short' : 'bi bi-arrow-up-short';
        }

        // Sort rows
        rows.sort((a, b) => {
            let aValue, bValue;
            
            if (column === 'Dzień urodzin' || column === 'Dzień imienin') {
                // Extract date from format "DD.MM"
                const aDate = a.cells[column === 'Dzień urodzin' ? 1 : 2].textContent;
                const bDate = b.cells[column === 'Dzień urodzin' ? 1 : 2].textContent;
                const [aDay, aMonth] = aDate.split('.').map(Number);
                const [bDay, bMonth] = bDate.split('.').map(Number);
                
                // Compare months first, then days
                if (aMonth !== bMonth) {
                    return newDirection === 'asc' ? aMonth - bMonth : bMonth - aMonth;
                }
                return newDirection === 'asc' ? aDay - bDay : bDay - aDay;
            } else {
                // For name column
                aValue = a.cells[0].textContent.trim();
                bValue = b.cells[0].textContent.trim();
                return newDirection === 'asc' 
                    ? aValue.localeCompare(bValue, 'pl')
                    : bValue.localeCompare(aValue, 'pl');
            }
        });

        // Reorder rows in the table
        rows.forEach(row => tbody.appendChild(row));
    }
}

// Automatyczna inicjalizacja komponentu
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing UserList...');
    new UserList();
});

// --- MODAL ADD USER LOGIC ---
import $ from 'jquery';

$(document).ready(function() {
    const modal = $('#add-user-modal');
    const btn = $('#add-user-button');
    const formContainer = $('#add-user-form-container');

    btn.click(function() {
        // Load form via AJAX
        $.ajax({
            url: '/users/add_ajax/',
            type: 'GET',
            success: function(data) {
                // Extract only the form from the response (if full page is returned)
                let formHtml = $(data).find('form').length ? $(data).find('form') : data;
                formContainer.html(formHtml);
                modal.show();
            },
            error: function() {
                alert('Nie udało się załadować formularza.');
            }
        });
    });

    // Close modal on X click or outside
    modal.on('click', '.close', function() {
        modal.hide();
        formContainer.empty();
    });
    $(window).on('click', function(event) {
        if (event.target === modal[0]) {
            modal.hide();
            formContainer.empty();
        }
    });

    // Delegate submit for dynamically loaded form
    formContainer.on('submit', 'form', function(event) {
        event.preventDefault();
        const form = $(this);
        const formData = form.serialize();
        $.ajax({
            url: '/users/add_ajax/',
            type: 'POST',
            data: formData,
            success: function(data, status, xhr) {
                // If response is HTML, assume success and new user row is returned
                if (xhr.getResponseHeader('Content-Type').includes('text/html')) {
                    // Add new user row to table
                    const newRow = $(data).find('tr').length ? $(data).find('tr') : data;
                    // Find tbody and append
                    $('table tbody').append(newRow);
                    // Re-bind clickable row handler for new rows
                    new UserList().setupClickableRows();
                    modal.hide();
                    formContainer.empty();
                } else {
                    // If JSON, show errors
                    alert('Nie udało się dodać użytkownika.');
                }
            },
            error: function(xhr) {
                // Show form with errors
                let formHtml = $(xhr.responseText).find('form').length ? $(xhr.responseText).find('form') : xhr.responseText;
                formContainer.html(formHtml);
            }
        });
    });
}); 