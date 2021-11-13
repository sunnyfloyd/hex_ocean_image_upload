from image_hoarder.config.common import ALLOWED_IMAGE_EXTENSIONS
from django.core.exceptions import ValidationError


# I could not use a wrapped validator with extensions passed in the model
# declaration. Validator was working properly, but `makemigrations` was raising
# an exception.


def validate_image_extension(image):
    splitted_name = image.name.split(".")

    if len(splitted_name) < 2:
        raise ValidationError("Image file needs to have an extension.")

    image_extension = splitted_name[-1].lower()
    if image_extension not in [ext.lower() for ext in ALLOWED_IMAGE_EXTENSIONS]:
        raise ValidationError(
            f"Only following image extensions are allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
