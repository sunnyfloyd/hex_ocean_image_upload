from rest_framework import serializers
from rest_framework import exceptions
from image_hoarder.images.models import Image, TempLink, Upload
from image_hoarder.config.common import HOSTNAME
from image_hoarder.images.thumbnails import create_thumbnails


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail_option = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Image
        fields = (
            "thumbnail_option",
            "image",
        )

    def get_image(self, obj):
        return HOSTNAME + obj.image.url


class UploadSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Upload
        fields = ("id", "user", "images")


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "upload", "image", "thumbnail_option", "is_original")  # '_all_'
        read_only_fields = ("upload", "thumbnail_option", "is_original")

    def save(self, **kwargs):
        user = kwargs.pop("user", None)
        if user is None:
            raise exceptions.ValidationError(
                "User needs to be passed to the serializer."
            )

        upload = Upload.objects.create(user=user)
        keep_original = user.plan.keep_original

        if keep_original:
            image = super().save(**kwargs)
            image.upload = upload
            image.save()
        else:
            validated_data = {**self.validated_data, **kwargs}
            image = Image(**validated_data)

        create_thumbnails(image, user, upload)

        return upload


class TempLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempLink
        fields = "__all__"

    def validate_upload(self, upload):
        user = self.context["request"].user

        if upload.user != user:
            raise serializers.ValidationError(
                "Only user who uploaded an image can create a temporary link for it."
            )

        if not user.plan.has_expiry_link:
            raise serializers.ValidationError(
                "Your plan does not allow for temporary link creation."
            )

        try:
            upload.images.get(thumbnail_option=None)
        except Image.DoesNotExist:
            raise serializers.ValidationError(
                "There is no original image to which link can be created."
            )

        return upload
