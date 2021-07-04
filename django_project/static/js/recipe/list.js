function buildParametersUrl(params) {
    let url = '?';
    for (let [k, v] of Object.entries(params)) {
        url += `${k}=${v}&`;
    }
    return url;
}

$(document).ready(() => {
    const path = window.location.pathname;
    const previousLink = $('#prev-page');
    const nextLink = $('#next-page');
    const previousPage = parseInt(previousLink.attr('href'));
    const nextPage = parseInt(nextLink.attr('href'));
    if (path.includes('/recipe/')) {
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
    if (path.includes('/category/')) {
        if (previousPage) {
            previousLink.attr('href', `?page=${previousPage}`);
        }
        if (nextPage) {
            nextLink.attr('href', `?page=${nextPage}`);
        }
    }
});