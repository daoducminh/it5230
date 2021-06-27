function buildParametersUrl(params) {
    let url = '?';
    for (let [k, v] of Object.entries(params)) {
        url += `${k}=${v}&`;
    }
    return url;
}

$(document).ready(() => {
    if ($('#filter-div').length) {
        const previousLink = $('#prev-page');
        const nextLink = $('#next-page');
        const previousPage = parseInt(previousLink.attr('href'));
        const nextPage = parseInt(nextLink.attr('href'));
        const search = location.search.substring(1);
        const params = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g, '":"') + '"}');
        delete params.page;
        const url = buildParametersUrl(params);
        if (previousPage) {
            previousLink.attr('href', url + `page=${previousPage}`);
        }
        if (nextPage) {
            nextLink.attr('href', url + `page=${nextPage}`);
        }
    }
    const lazyImageInputs = $('.lazy-image-input');
    for (let i = 0; i < lazyImageInputs.length; i++) {
        const imageUrl = $(lazyImageInputs[i]).val();
        const parent = $(lazyImageInputs[i].parentElement);
        const image = parent.find('img');
        $(image).attr('src', imageUrl);
    }
});