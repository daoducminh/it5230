$(function () {
    $('[data-toggle="tooltip"]').tooltip();
})

$(document).ready(() => {
    const searchType = $('#search-type');
    const searchForm = $('#search-form');
    searchForm.prop('action', `/${searchType.val()}/`);
    searchType.change(() => {
        searchForm.prop('action', `/${searchType.val()}/`);
    })
});