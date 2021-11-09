import uuid
from rest_framework import serializers
from rest_framework import exceptions
from image_hoarder.images.models import Image, Upload
import PIL
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        # fields = ('id', 'upload', 'image', 'thumbnail', 'is_original')
        fields = ('id', 'upload', 'image', 'thumbnail_option', 'is_original')  # '_all_'
        read_only_fields = ('upload', 'thumbnail_option', 'is_original')


    def get_scaled_size(self, current_size, thumbnail_height):
        current_width, current_height = current_size
        scale = int(round(current_height / thumbnail_height, 0))
        thumbnail_width = int(round(current_width / scale, 0))
        
        return (thumbnail_width, thumbnail_height)


    def generate_thumb(self, original, height, format='JPEG'):
        """
        Generates a thumbnail image and returns a ContentFile object with the thumbnail
        Arguments:
        original -- The image being resized as `File`.
        height     -- Desired thumbnail height.
        format   -- Format of the original image ('JPEG', 'PNG', ...) The thumbnail will be generated using this same format.
        """
        original.seek(0)
        image = PIL.Image.open(original)
        current_size = image.size
        size = self.get_scaled_size(current_size, height)

        if image.mode not in ('L', 'RGB', 'RGBA'):
            image = image.convert('RGB')
        thumbnail = PIL.ImageOps.fit(image, size, PIL.Image.ANTIALIAS)
        io = BytesIO()
        thumbnail.save(io, format)
        
        return ContentFile(io.getvalue())

    
    def save(self, **kwargs):
        user = kwargs.pop('user', None)
        if user is None:
            raise exceptions.ValidationError("No uses has been passed to the serializer.")
        image = super().save(**kwargs)

        # create new user upload
        upload = Upload.objects.create(user=user)
        image.upload = upload
        image.save()

        # create thumbnails
        original_img = image.image.open()
        thumbnail_options = user.plan.thumbnail_options.all()

        for thumbnail_option in thumbnail_options:
            # img_height = thumbnail_option.height
            # image.image.open()
            # original_img = PIL.Image.open(image.image)
            # w, h = original_img.size
            # scale = int(round(h / img_height, 0))
            # img_width = int(round(w * scale, 0))
            # thumbnail = original_img.resize((img_width, img_height), PIL.Image.ANTIALIAS)
            # image_file = StringIO()
            # thumbnail.save(image_file, 'JPEG', quality=90)
            # image_file = BytesIO()
            # thumbnail.save(image_file, 'JPEG', quality=90)
            # Image.objects.create(upload=upload, image=image_file, thumbnail_option=thumbnail_option, is_original=False)

            thumbnail_height = thumbnail_option.height
            content = self.generate_thumb(original_img, thumbnail_height)
            storage = get_storage_class()()
            saved_as = storage.save(str(uuid.uuid4()) + '.jpg', content)

            Image.objects.create(
                upload=upload,
                image=saved_as,
                thumbnail_option=thumbnail_option,
                is_original=False
            )
        
        return image
