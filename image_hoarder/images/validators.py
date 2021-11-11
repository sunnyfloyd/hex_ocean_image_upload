from django.core.exceptions import ValidationError

def validate_image_extension(allowed_extensions):
    def inner_validator(image):
        splitted_name = image.name.split('.')

        if len(splitted_name) < 2:
            raise ValidationError("Image file needs to have an extension.")

        image_extension = splitted_name[-1].lower()
        if image_extension not in [ext.lower() for ext in allowed_extensions]:
            raise ValidationError(
                f"Only following image extensions are allowed: {', '.join(allowed_extensions)}"
            )
    
    return inner_validator
