$(document).ready(() => {
    const lazyImageInputs = $('.lazy-image-input');
    for (let i = 0; i < lazyImageInputs.length; i++) {
        const imageUrl = $(lazyImageInputs[i]).val();
        const parent = $(lazyImageInputs[i].parentElement);
        const image = parent.find('img');
        $(image).attr('src', imageUrl);
    }
});