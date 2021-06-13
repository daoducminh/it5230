function switchDeleteButton(state) {
    const button = $('#confirm-delete');
    button.empty();
    button.prop('disabled', !state);
    if (state) {
        button.text('Yes');
    } else {
        button.html('<span class="spinner-border spinner-border-sm mr-2"></span>Loading...');
    }
}

function showDeleteResult(message, status) {
    const deleteModal = $('#delete-modal');
    const messageModal = $('#message-modal');
    const messageContent = $('#message-content');
    messageContent.text(message);
    if (status) {
        messageContent.attr('class', 'alert alert-success');
    } else {
        messageContent.attr('class', 'alert alert-danger');
    }
    deleteModal.modal('hide');
    messageModal.modal('show');
    setTimeout(() => {
        window.location.href = document.referrer;
    }, 3000);
}

$(document).ready(() => {
    $('#confirm-delete').click(() => {
        const deleteURL = window.location.pathname + 'delete/';

        $.ajax({
            type: 'POST',
            url: deleteURL,
            beforeSend: () => {
                switchDeleteButton(false);
            },
            success: (data) => {
                switchDeleteButton(true);
                showDeleteResult(data.message, true);
            },
            error: (error) => {
                switchDeleteButton(true);
                showDeleteResult(error.message, false);
            }
        });
    })
});