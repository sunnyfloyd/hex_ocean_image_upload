from image_hoarder.config.common import IMAGE_UPLOAD_DIR
import os


def get_file_path(instance, filename):
    """
    Overrides default ImageField file naming.
    """
    ext = filename.split('.')[-1]
    filename = f'{instance.id}.{ext}'
    return os.path.join(IMAGE_UPLOAD_DIR, filename)
