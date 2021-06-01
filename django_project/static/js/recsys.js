$(document).ready(() => {
    $.get('/rec/recipe/' + uid, (result, error) => {
        data = JSON.parse(result.data)
        console.log(data)
        for (let i = 0; i < data.length; i++) {
            rid = data[i].pk
            d = data[i].fields
            let imageUrl = '/media/default.jpg';
            if (d.image_url) {
                imageUrl = d.image_url;
            }
            $('#svd').append(`<div class="col-3">
<div class="card">
<div class="card-header text-center">
<a href="/recipe/${rid}">
<img src="${imageUrl}" class="img-fluid card-img-top">
</a>
</div>
<div class="card-body">
<h5 class="card-title text-truncate">
<a href="/recipe/${rid}">${d.recipe_name}</a>
</h5>
</div>
</div>
</div>`)
        }
    })
})