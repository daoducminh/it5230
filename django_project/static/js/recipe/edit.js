let imageTab = true;
const urlRegex = /[-a-zA-Z0-9@:%_+.~#?&/=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_+.~#?&/=]*)?/gi;

function previewImageUrl(initial) {
    const inputImageUrl = $('#image-url');
    const imageUrl = inputImageUrl.val();
    const container = $('#preview-image-url');
    if (imageUrl) {
        if (imageUrl.match(urlRegex)) {
            container.html(`<img src="${imageUrl}" class="img-fluid img-thumbnail" alt="Image is invalid">`);
        } else {
            container.html('<div class="alert alert-danger">Invalid image url.</div>')
        }
    } else if (initial) {
        container.html('<div class="alert alert-danger">Please input your image url.</div>')
    }
}

function previewImage() {
    const inputImage = $('#image');
    const [file] = inputImage[0].files;
    const container = $('#preview-image');
    if (file) {
        const src = URL.createObjectURL(file);
        container.html(`<img src="${src}" class="img-fluid img-thumbnail" alt="Image is invalid">`);
    }
}

function activeTab(tab) {
    $('.nav-tabs a[href="#' + tab + '"]').tab('show');
}

function switchImageTab(state) {
    if (imageTab !== state) {
        imageTab = state;
        if (state) {
            activeTab('tab-image');
        } else {
            activeTab('tab-image-url');
        }
    }
}

function submitRecipe() {
    if (imageTab) {
        $('#image-url').val('');
    } else {
        $('#image').val('');
    }
    $('#recipe-form').submit();
}

$(document).ready(() => {
    $.fn.selectpicker.Constructor.BootstrapVersion = '4';
    // Switch image tab event
    $('#nav-image').click(() => {
        switchImageTab(true);
    })
    $('#nav-image-url').click(() => {
        switchImageTab(false);
    })
    // Preview image on update
    const hiddenImageUrl = $('#hidden-image-url').val();
    const imageUrl = $('#image-url').val();

    if (hiddenImageUrl) {
        $('#preview-image').html(`<img src="${hiddenImageUrl}" class="img-fluid img-thumbnail" alt="Image is invalid">`);
        switchImageTab(true);
    }
    if (imageUrl) {
        $('#preview-image-url').html(`<img src="${imageUrl}" class="img-fluid img-thumbnail" alt="Image is invalid">`);
        switchImageTab(false);
    }

    // Preview image events
    $('#image').change(previewImage);
    $('#btn-preview').click(previewImageUrl);

    // Submit event
    $('#btn-submit').click(submitRecipe);
});