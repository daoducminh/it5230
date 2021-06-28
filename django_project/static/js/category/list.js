$(document).ready(() => {
    const updateModal = $('#update-modal');
    const updateForm = $('#update-form');
    const inputTitle = $('#input-title');
    const inputShortName = $('#input-short-name');
    $('.category-button').click(function () {
        const id = $(this).find('input#id').val();
        const title = $(this).find('input#title').val();
        const shortName = $(this).find('input#short-name').val();
        $(inputTitle).val(title);
        $(inputShortName).val(shortName);
        $(updateForm).attr('action', `${id}/update/`);
        $(updateModal).modal('show');
    })
})