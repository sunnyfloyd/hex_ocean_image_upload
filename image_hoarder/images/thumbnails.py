import PIL
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
import uuid
from image_hoarder.images.models import Image


def calculate_scaled_size(current_size, thumbnail_height):
    """
    Calculates scaled size for a thumbnail.

    Args:
        current_size: A tuple with current image size.
        thumbnail_height: An integer designating current image height.

    Returns:
        A tuple with thumbnail width and height.
    """

    current_width, current_height = current_size
    scale = int(round(current_height / thumbnail_height, 0))
    thumbnail_width = int(round(current_width / scale, 0))
    
    return (thumbnail_width, thumbnail_height)


def generate_thumb(original, height, format='JPEG'):
    """
    Generates and returns a thumbnail image.
    
    Args:
        original: The image being resized as `File`.
        height: Desired thumbnail height.
        format: Format of the original image ('JPEG', 'PNG').
          The thumbnail will be generated using this same format.

    Returns:
        A ContentFile object with the thumbnail.
    """

    original.seek(0)
    image = PIL.Image.open(original)
    current_size = image.size
    size = calculate_scaled_size(current_size, height)
    format = "JPEG" if format.lower() == 'jpg' else format

    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    thumbnail = PIL.ImageOps.fit(image, size, PIL.Image.ANTIALIAS)
    io = BytesIO()
    thumbnail.save(io, format)
    
    return ContentFile(io.getvalue())


def create_thumbnails(image, user, upload):
    """
    Creates thumbnails based on provided image and links them
    to the single upload.

    Args:
        image: An instance of an Image containing uploaded image file.
        user: An instance of a User who made an upload.
        upload: An instance of an Upload that links original file and thumbnails.
    """

    original_img = image.image.open()
    format = image.image.name.split('.')[-1]
    thumbnail_options = user.plan.thumbnail_options.all()

    for thumbnail_option in thumbnail_options:
        thumbnail_height = thumbnail_option.height
        content = generate_thumb(original_img, thumbnail_height, format)
        storage = get_storage_class()()
        saved_as = storage.save(str(uuid.uuid4()) + f'.{format.lower()}', content)

        Image.objects.create(
            upload=upload,
            image=saved_as,
            thumbnail_option=thumbnail_option,
            is_original=False
        )
