import os
import uuid
from django.utils.text import slugify
from unidecode import unidecode

def get_upload_path(instance: str, filename: str):
    """
    Генерирует динамический путь для загрузки файлов.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(instance.__class__.__name__.lower(), filename)