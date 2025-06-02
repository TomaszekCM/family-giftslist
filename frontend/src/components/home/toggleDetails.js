import $ from 'jquery';

// function to show hidden gift data
$('#gift-list').on('click', '.toggle-details', function(e) {
    e.preventDefault();
    $(this).next('.gift-details').slideToggle();
});