const recipes = new Set();

function switchRecipeButton(id, state) {
    const buttonId = `#r-${id}`;
    const button = $(buttonId);
    if (state) {
        button.text('Added');
        button.removeClass('btn-primary');
        button.addClass('btn-secondary');
        button.prop('disabled', true);
    } else {
        button.text('Add');
        button.removeClass('btn-secondary');
        button.prop('disabled', false);
        button.addClass('btn-primary');
    }
}

function removeRecipe(id) {
    recipes.delete(id);
    switchRecipeButton(id, false);
}

function switchSubmitButton(state) {
    const button = $('#btn-submit');
    button.empty();
    button.prop('disabled', !state);
    if (state) {
        button.text('Save');
    } else {
        button.html('<span class="spinner-border spinner-border-sm mr-2"></span>Loading...');
    }
}

function showSubmitResult(message, status) {
    const messageModal = $('#message-modal');
    const messageContent = $('#message-content');
    messageContent.text(message);
    if (status) {
        messageContent.attr('class', 'alert alert-success');
    } else {
        messageContent.attr('class', 'alert alert-danger');
    }
    messageModal.modal('show');
    setTimeout(() => {
        window.location.href = document.referrer;
    }, 3000);
}

function submitMenu() {
    const menuName = $('#menu-name').val();
    const description = $('#description').val();
    const data = {
        menuName: menuName,
        description: description,
        recipes: Array.from(recipes)
    }
    $.ajax({
        type: 'POST',
        url: window.location.pathname,
        data: JSON.stringify(data),
        contentType: 'application/json',
        beforeSend: () => {
            switchSubmitButton(false);
        },
        success: (data) => {
            switchSubmitButton(true);
            showSubmitResult(data.message, true);
        },
        error: (error) => {
            switchSubmitButton(true);
            showSubmitResult('There is an error when submitting your menu.');
        }
    });
}