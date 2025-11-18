def get_path_upload_photo(instance, file):
    return f'photos/perevel_{instance.pereval.id}/{file}'