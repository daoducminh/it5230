let recipeData = null;

function addRecipe(index) {
    const r = recipeData[index];
    const id = r['id'];
    if (recipes.has(id)) {
        console.log('Recipe has been added');
    } else {
        switchRecipeButton(id, true);

        const element = `<div class="alert alert-dismissible fade show">
    ${r['recipe_name']}
    <button type="button" class="btn btn-danger" data-dismiss="alert" onclick="removeRecipe(${r['id']})">Remove</button>
    <input type="hidden" value="${r['id']}">
</div>`;
        $('#recipe-list').append(element);
        recipes.add(r['id'])
    }
}

$(document).ready(() => {
    $('#btn-submit').click(submitMenu);
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
    $('button#btn-search').click(() => {
        const name = $('#input-recipe').val();
        if (name) {
            const resultBox = $('#search-result');

            $.get(
                '/search/',
                {'name': name},
                (data) => {
                    recipeData = data;
                    for (let i = 0; i < data.length; i++) {
                        const r = data[i];
                        const id = r['id']
                        if (recipes.has(id)) {
                            const element = `<div class="alert alert-dismissible fade show">
    ${r['recipe_name']}
    <button type="button" class="btn btn-secondary" disabled onclick="addRecipe(${i})" id="r-${id}">Added</button>
</div>`;
                            resultBox.append(element);
                        } else {
                            const element = `<div class="alert alert-dismissible fade show">
    ${r['recipe_name']}
    <button type="button" class="btn btn-success" onclick="addRecipe(${i})" id="r-${id}">Add</button>
</div>`;
                            resultBox.append(element);
                        }
                    }
                }
            );
        }
    })
})