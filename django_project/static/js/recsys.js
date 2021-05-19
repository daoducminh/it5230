$(document).ready(() => {
    $.get('/rec/recipe/' + uid, (result, error) => {
        data = JSON.parse(result.data)
        console.log(data)
        for (let i = 0; i < data.length; i++) {
            rid = data[i].pk
            d = data[i].fields
            $('#knn').append(`<div class="col-3">
<div class="card">
<div class="card-header text-center">
<a href="/dish/${rid}">
<img src="${d.image_url}" alt="/media/default.jpg" height="200">
</a>
</div>
<div class="card-body">
<h5 class="card-title text-truncate">
<a href="/dish/${rid}">${d.dish_name}</a>
<p class="card-text text-truncate">${d.description}</p>
</h5>
</div>
</div>
</div>`)
        }
    })
})