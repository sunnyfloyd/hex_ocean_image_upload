from rest_framework import serializers
from image_hoarder.images.models import Image

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ('id', 'user', 'image')
