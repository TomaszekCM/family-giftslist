import $ from 'jquery';

$(function() {
    const modal = $('#edit-profile-modal');
    const editBtn = $('#edit-profile-btn');
    const closeBtn = $('.close');

    // Opening modal and loading form
    editBtn.on('click', function() {
        $.get('/get_user_data_form/', function(data) {
            $('#user-data-form-container').html(data);
            modal.css('display', 'block');
        });
    });

    // Closing modal by clicking X
    closeBtn.on('click', function() {
        modal.css('display', 'none');
    });

    // Closing modal by clicking outside of it
    $(window).on('click', function(event) {
        if (event.target === modal[0]) {
            modal.css('display', 'none');
        }
    });

    // Handling form
    $(document).on('submit', '#edit-user-data-form', function(event) {
        event.preventDefault();

        $.ajax({
            url: '/edit_user_data/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    location.reload();
                }
            },
            error: function(xhr) {
                const errors = xhr.responseJSON?.errors;
                if (errors) {
                    alert(Object.values(errors).flat().join('\n'));
                } else {
                    alert("Wystąpił błąd podczas zapisywania danych");
                }
            }
        });
    });
}); 