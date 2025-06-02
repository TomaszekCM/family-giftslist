import $ from 'jquery';

// DELETE BUTTON
$(document).on('click', '.delete-gift-btn', function(e) {
    e.preventDefault();

    const button = $(this);
    const giftId = button.data('gift-id');
    const giftName = button.data('gift-name');

    if (confirm(`Czy na pewno chcesz usunąć prezent "${giftName}"?`)) {
        $.ajax({
            url: '/delete_gift/',
            type: 'POST',
            data: {
                gift_id: giftId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.success) {
                    button.closest('.gift-preview').remove();
                }
            },
            error: function() {
                alert("Wystąpił błąd podczas usuwania prezentu.");
            }
        });
    }
});