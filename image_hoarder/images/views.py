from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from image_hoarder.images.models import Upload, Image, TempLink
from image_hoarder.images.serializers import (
    ImageUploadSerializer,
    UploadSerializer,
    TempLinkSerializer,
)
from image_hoarder.images.viewsets import MultiSerializerViewSet
from rest_framework import mixins
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework import exceptions
from rest_framework import viewsets
import datetime
from django.utils import timezone


class UploadViewSet(MultiSerializerViewSet):
    """
    Creates, retrieves and lists uploads
    """

    queryset = Upload.objects.all()
    serializers = {
        "create": ImageUploadSerializer,
        "default": UploadSerializer,
    }
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        upload = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # returning serialized upload instance instead of an image one
        return Response(
            UploadSerializer(upload).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        # returning upload instance
        return serializer.save(user=self.request.user)


class TempLinkCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = TempLink.objects.all()
    serializer_class = TempLinkSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)


@api_view(["GET"])
def temporary_content(request, pk):
    temp_link = get_object_or_404(TempLink, pk=pk)
    expiration_date = temp_link.created + datetime.timedelta(
        seconds=temp_link.expiry_after
    )

    if expiration_date < timezone.now():
        raise exceptions.NotFound()

    image = get_object_or_404(temp_link.upload.images, thumbnail_option=None)

    return HttpResponse(image.image, content_type="image/jpg")
