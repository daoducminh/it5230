import os


def validate_image_extension(value):
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', 'jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
