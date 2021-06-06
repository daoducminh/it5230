let recipeData = null;

function addRecipe(index) {
    const r = recipeData[index];
    const id = r['id'];
    if (recipes.has(id)) {
        console.log('Recipe has been added');
    } else {
        // Switch button
        switchRecipeButton(id, true);

        // Append element
        let image;
        const score = Math.round(r['score']);
        const numberReview = r['review_number'];
        const starRating = generateRatingStars(score);
        const recipeList = $('#recipe-list');

        if (r['image']) {
            image = r['image'];
        } else if (r['image_url']) {
            image = r['image_url'];
        } else {
            image = '/media/default.jpg';
        }

        const element = `<div class="alert alert-dismissible fade show recipe-item">
    <div class="row">
        <div class="col-3 recipe-img">
            <img src="${image}" alt="" class="img-fluid img-thumbnail">
        </div>
        <div class="col-9 d-flex flex-column justify-content-between">
            <div>${r['recipe_name']}</div>
            <div>${starRating} <span class="text-danger">(${numberReview})</span></div>
        </div>
    </div>
    <div><button type="button" class="btn-remove-recipe" data-dismiss="alert" aria-label="close" onclick="removeRecipe(${r['id']})">&times;</button></div>
    <input type="hidden" value="${r['id']}">
</div>`;
        recipeList.append(element);
        recipeList.animate({scrollTop: recipeList.prop("scrollHeight")}, 500);
        recipes.add(r['id'])
    }
}

function generateRatingStars(score) {
    let result = '';
    for (let i = 0; i < score; i++) {
        result += '<i class="fas fa-star fa-star-gold"></i>';
    }
    for (let i = 0; i < 5 - score; i++) {
        result += '<i class="far fa-star fa-star-gold"></i>';
    }
    return result;
}

function searchRecipe() {
    const name = $('#input-recipe').val();
    if (name) {
        const resultBox = $('#search-result');

        $.get(
            '/search/',
            {'name': name},
            (data) => {
                recipeData = data;
                // Clear old result elements
                resultBox.empty();

                // Append new result elements
                for (let i = 0; i < data.length; i++) {
                    const r = data[i];
                    const id = r['id'];
                    const score = Math.round(r['score']);
                    const numberReview = r['review_number'];
                    const starRating = generateRatingStars(score);
                    let button, image;
                    if (recipes.has(id)) {
                        button = `<button type="button" class="btn btn-secondary" disabled onclick="addRecipe(${i})" id="r-${id}">Added</button>`;
                    } else {
                        button = `<button type="button" class="btn btn-success" onclick="addRecipe(${i})" id="r-${id}">Add</button>`;
                    }
                    if (r['image']) {
                        image = r['image'];
                    } else if (r['image_url']) {
                        image = r['image_url'];
                    } else {
                        image = '/media/default.jpg';
                    }
                    const element = `<div class="alert alert-dismissible recipe-item">
    <div class="row">
        <div class="col-3 recipe-img">
            <img class="img-fluid img-thumbnail" src="${image}" alt="">
        </div>
        <div class="col-9 d-flex flex-column justify-content-between">
            <div>${r['recipe_name']}</div>
            <div>${starRating} <span class="text-danger">(${numberReview})</span></div>
        </div>
    </div>
    ${button}
</div>`;
                    resultBox.append(element);
                }
            }
        );
    }
}

$(document).ready(() => {
    // Submit menu event
    $('#btn-submit').click(submitMenu);

    // Scan existed recipes and add to set
    const recipeList = $('#recipe-list > div > input');
    if (recipeList.length > 0) {
        for (let i = 0; i < recipeList.length; i++) {
            try {
                let x = parseInt(recipeList[i].value);
                recipes.add(x);
            } catch (error) {
                console.log(error)
            }
        }
    }

    // Search box on press enter event
    $('#input-recipe').on('keypress', (e) => {
        if (e.which === 13) {
            searchRecipe();
        }
    });

    // Search button on click event
    $('button#btn-search').click(searchRecipe)
})