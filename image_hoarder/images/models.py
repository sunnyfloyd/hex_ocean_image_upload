import uuid
from django.db import models
from django.core.validators import MinValueValidator
from rest_framework.reverse import reverse
from image_hoarder.config.common import HOSTNAME


class ThumbnailOption(models.Model):
    height = models.IntegerField(
        validators=[MinValueValidator(100)],
        unique=True
    )

    def __str__(self) -> str:
        return f"Thumbnail height: {self.height}"


class Upload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="uploads"
    )

    def __str__(self) -> str:
        return f'{self.id} uploaded by {self.user.username}'

    def get_absolute_url(self):
        return reverse("upload-detail", kwargs={"pk": self.pk})


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload = models.ForeignKey(
        "images.Upload",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="images"
    )
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    thumbnail_option = models.ForeignKey(
        "images.ThumbnailOption",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="images"
    )
    is_original = models.BooleanField(default=True)

    def __str__(self) -> str:
        return HOSTNAME + self.image.url

    def get_absolute_url(self):
        return reverse("image-detail", kwargs={"pk": self.pk})
    
