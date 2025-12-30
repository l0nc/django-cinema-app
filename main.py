import os
import uuid



def get_upload_path(instance, filename: str):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(instance.__class__.__name__.lower(), filename)

a = [(i, str(i)) for i in range(1, 11)]
print(a)