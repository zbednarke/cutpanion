from django.core.files.storage import default_storage
from os import path


def get_storage_url(file_path):
    base_url = default_storage.client._base_connection.API_BASE_URL
    return path.join(base_url, default_storage.bucket_name, file_path)