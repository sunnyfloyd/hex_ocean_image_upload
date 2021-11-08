import uuid
from django.db import models
from django.core.validators import MinValueValidator


class Thumbnail(models.Model):
    height = models.IntegerField(
        validators=[MinValueValidator(100)],
        unique=True
    )

    def __str__(self) -> str:
        return f"Thumbnail height: {self.height}"


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="images")

    def __str__(self) -> str:
        return f"Image {self.id} uploaded by {self.user}"
