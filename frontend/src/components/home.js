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
            }
        });
    });
});
