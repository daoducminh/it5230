def dish_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{0}.{1}'.format(instance.pk, ext)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
