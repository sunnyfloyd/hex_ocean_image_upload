from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from image_hoarder.images.models import Image, Upload
from image_hoarder.images.serializers import ImageSerializer, UploadSerializer
from image_hoarder.images.viewsets import MultiSerializerViewSet


class UploadViewSet(MultiSerializerViewSet):
    """
    Creates, retrieves and lists uploads
    """
    queryset = Upload.objects.all()
    serializers = {
        'create': ImageSerializer,
        'default': UploadSerializer,
    }
    permission_classes = (IsAuthenticated,)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        upload = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # returning serialized upload instance instead of an image one
        return Response(UploadSerializer(upload).data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        # returning upload instance
        return serializer.save(user=self.request.user)
