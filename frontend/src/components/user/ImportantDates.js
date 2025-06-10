import $ from 'jquery';

$(function() {
    const modal = $('#important-date-modal');
    const addBtn = $('#add-date-btn');
    let currentEditingDateId = null;

    // Opening modal and loading form for adding
    addBtn.on('click', function() {
        currentEditingDateId = null;
        modal.find('h2').text('Ważna data');
        $.get('/get_important_date_form/', function(data) {
            $('#important-date-form-container').html(data);
            modal.css('display', 'block');
        });
    });

    // Opening modal and loading form for editing
    $(document).on('click', '.edit-date-btn', function() {
        const dateId = $(this).data('date-id');
        currentEditingDateId = dateId;
        modal.find('h2').text('Edytuj datę');
        $.get(`/get_important_date_form/${dateId}/`, function(data) {
            $('#important-date-form-container').html(data);
            modal.css('display', 'block');
        });
    });

    // Get CSRF token from the form
    function getCsrfToken() {
        return $('#important-date-form-container input[name="csrfmiddlewaretoken"]').val();
    }

    // Handling date deletion
    $(document).on('click', '.delete-date-btn', function() {
        const dateId = $(this).data('date-id');
        const dateName = $(this).closest('.list-group-item').find('.text-muted').text();
        
        if (confirm(`Czy na pewno chcesz usunąć datę "${dateName}"?`)) {
            // First, load the form to get a fresh CSRF token
            $.get('/get_important_date_form/', function() {
                const csrfToken = getCsrfToken();
                
                $.ajax({
                    url: `/delete_important_date/${dateId}/`,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    success: function(response) {
                        if (response.success) {
                            $(`.delete-date-btn[data-date-id="${dateId}"]`)
                                .closest('.list-group-item')
                                .remove();
                        }
                    },
                    error: function() {
                        alert('Wystąpił błąd podczas usuwania daty');
                    }
                });
            });
        }
    });

    // Closing modal by clicking X or Cancel button
    $(document).on('click', '.modal-close', function() {
        modal.css('display', 'none');
    });

    // Closing modal by clicking outside of it
    $(window).on('click', function(event) {
        if (event.target === modal[0]) {
            modal.css('display', 'none');
        }
    });

    // Form submission
    $(document).on('submit', '#important-date-form', function(e) {
        e.preventDefault();
        
        const url = currentEditingDateId 
            ? `/edit_important_date/${currentEditingDateId}/`
            : '/add_important_date/';

        $.ajax({
            url: url,
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.status === 'success') {
                    const dateHtml = `
                        <div class="list-group-item d-flex justify-content-between align-items-center border-0 border-bottom border-light-subtle">
                            <div class="d-flex align-items-center gap-3">
                                <strong>${response.date.date}</strong>
                                <span class="text-muted">${response.date.name}</span>
                            </div>
                            <div class="btn-group">
                                <button class="btn btn-sm btn-outline-secondary edit-date-btn" data-date-id="${response.date.id}">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger delete-date-btn" data-date-id="${response.date.id}">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        </div>`;
                    
                    if (currentEditingDateId) {
                        // Update existing date
                        $(`.edit-date-btn[data-date-id="${currentEditingDateId}"]`)
                            .closest('.list-group-item')
                            .replaceWith(dateHtml);
                    } else {
                        // Add new date
                        $('#add-date-btn').closest('.list-group-item').before(dateHtml);
                    }
                    modal.css('display', 'none');
                }
            },
            error: function(xhr) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    if (response.errors) {
                        alert(Object.values(response.errors).flat().join('\n'));
                    } else {
                        alert("Wystąpił błąd podczas zapisywania daty");
                    }
                } catch (e) {
                    console.error('Error parsing response:', e);
                    alert("Wystąpił błąd podczas zapisywania daty");
                }
            }
        });
    });
}); 