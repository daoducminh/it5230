const recipes = new Set();

function switchRecipeButton(id, status) {
    const buttonId = `#r-${id}`;
    const button = $(buttonId);
    if (status) {
        button.text('Added');
        button.removeClass('btn-success');
        button.addClass('btn-secondary');
        button.prop('disabled', true);
    } else {
        button.text('Add');
        button.removeClass('btn-secondary');
        button.prop('disabled', false);
        button.addClass('btn-success');
    }
}

function removeRecipe(id) {
    recipes.delete(id);
    switchRecipeButton(id, false);
}

function submitMenu() {
    const menuName = $('#menu-name').val();
    const description = $('#description').val();
    const data = {
        menuName: menuName,
        description: description,
        recipes: Array.from(recipes)
    }
    $.ajax(
        window.location.pathname,
        {
            data: JSON.stringify(data),
            type: 'POST',
            contentType: 'application/json'
        }
    ).done((result) => {
        console.log(result.message);
    });
}