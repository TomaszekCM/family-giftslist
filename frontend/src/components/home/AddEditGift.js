import $ from 'jquery';


let currentEditingGiftId = null;

$(document).on('click', '.edit-gift-btn', function(e) {
    e.preventDefault();

    const giftElement = $(this).closest('.gift-preview');
    currentEditingGiftId = $(this).data('gift-id');

    $('#id_name').val(giftElement.data('name-original'));
    $('#id_description').val(giftElement.data('description'));
    $('#id_priority').val(giftElement.data('priority'));
    $('#id_approx_price').val(giftElement.data('price'));
    $('#id_link_to_shop').val(giftElement.data('link'));
    $('#id_category').val(giftElement.data('category'));

    $('#add-gift-modal h2').text('Edytuj prezent');
    $('#gift-form-button').text("Zapisz");
    $('#add-gift-modal').css('display', 'block');
});


$(document).ready(function() {
    const modal = $('#add-gift-modal');
    const btn = $('#add-gift-button');

    // this shows form
    btn.click(function() {
        $('#add-gift-form')[0].reset();
        $('#add-gift-modal h2').text('Dodaj wymarzony prezent');
        $('#gift-form-button').text("Dodaj prezent");
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
        event.preventDefault();

        const isEditing = currentEditingGiftId !== null;
        const url = isEditing ? '/edit_gift/' : $('#add-gift-button').data('url');

        const formData = $(this).serializeArray();
        if (isEditing) {
            formData.push({name: 'gift_id', value: currentEditingGiftId});
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            success: function(data) {
                if (isEditing) {
                    $(`.edit-gift-btn[data-gift-id="${currentEditingGiftId}"]`)
                        .closest('.gift-preview')
                        .replaceWith(data);
                } else {
                    $('#gift-list').append(data);
                }

                $('#add-gift-form')[0].reset();
                $('#add-gift-modal').css('display', 'none');
                currentEditingGiftId = null;
            },
            error: function(xhr) {
                const errors = xhr.responseJSON?.errors;
                if (errors) {
                    alert(Object.values(errors).flat().join('\n'));
                } else {
                    alert("Wystąpił błąd");
                }
            }
        });
    });
});
