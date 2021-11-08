from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from image_hoarder.images.models import Image
from image_hoarder.images.serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    Creates, retrieves and lists uploaded images
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (AllowAny,)
