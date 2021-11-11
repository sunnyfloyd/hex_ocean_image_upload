from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from image_hoarder.images.models import Upload, Image, TempLink
from image_hoarder.images.serializers import ImageUploadSerializer, UploadSerializer
from image_hoarder.images.viewsets import MultiSerializerViewSet
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework import exceptions


class UploadViewSet(MultiSerializerViewSet):
    """
    Creates, retrieves and lists uploads
    """
    queryset = Upload.objects.all()
    serializers = {
        'create': ImageUploadSerializer,
        'default': UploadSerializer,
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
        return Response(UploadSerializer(upload).data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        # returning upload instance
        return serializer.save(user=self.request.user)

@api_view(['POST'])
def create_temporary_link(request, pk):
    expiry_after = request.POST.get('expiry_after', None)

    if expiry_after is None:
        raise exceptions.ValidationError(
            "'expiry_after' integer value needs to be included in request's body."
        )

    upload = get_object_or_404(Upload, pk=pk)
    user = request.user

    if upload.user != user:
        raise exceptions.PermissionDenied(
            "Only user who uploaded an image can create a temporary link for it."
        )
    
    image = get_object_or_404(Upload.images, thumbnail_option=None)

    temp_link = TempLink.objects.create(image=image, expiry_after=expiry_after)
    return Response({"temp_link": temp_link.get_absolute_url()}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def temporary_content(request, pk):
    temp_obj = get_object_or_404(TempLink, pk=pk)

    # walidacja linka tutaj

    image_obj = get_object_or_404(Image, pk=pk)
    return HttpResponse(image_obj.image, content_type="image/png")
