from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from image_hoarder.images.models import Image, TempLink, ThumbnailOption, Upload
from image_hoarder.images.serializers import ImageSerializer, ImageUploadSerializer
from image_hoarder.users.models import Plan, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import datetime
from freezegun import freeze_time


class ImageTestCase(APITestCase):
    def setUp(self):
        # Create thumbnails
        tn200 = ThumbnailOption.objects.create(height=200)
        tn400 = ThumbnailOption.objects.create(height=400)

        # Create plans
        plan_basic = Plan.objects.create(
            name="Basic", keep_original=False, has_expiry_link=False
        )
        plan_basic.thumbnail_options.add(tn200)

        plan_premium = Plan.objects.create(
            name="Premium", keep_original=True, has_expiry_link=False
        )
        plan_premium.thumbnail_options.add(tn200, tn400)

        plan_enterprise = Plan.objects.create(
            name="Enterprise", keep_original=True, has_expiry_link=True
        )
        plan_enterprise.thumbnail_options.add(tn200, tn400)

        # Create users
        self.user_basic = User.objects.create(
            username="basic", password="123", plan=plan_basic
        )
        self.user_premium = User.objects.create(
            username="premium", password="123", plan=plan_premium
        )
        self.user_enterprise = User.objects.create(
            username="enterprise", password="123", plan=plan_enterprise
        )

    def test_serializer_with_empty_data(self):
        serializer = ImageUploadSerializer(data={})
        self.assertEqual(serializer.is_valid(), False)

    def _create_image_upload_serializer(self, name):
        example_image = SimpleUploadedFile(
            name=name, content=open(name, 'rb').read(), content_type='image/jpeg'
        )

        data = {'image': example_image}
        return ImageUploadSerializer(data=data)

    def test_serializer_with_valid_data(self):
        serializer = (
            self._create_image_upload_serializer(
                "example.jpg"
            )
        )

        self.assertEqual(serializer.is_valid(), True)
        serializer.is_valid()

        upload = serializer.save(user=self.user_basic)

    def test_image_upload_with_allowed_extension(self):
        serializer = (
            self._create_image_upload_serializer(
                "example.jpg"
            )
        )

        serializer.is_valid()

        upload = serializer.save(user=self.user_basic)
        self.assertEqual(upload.images.count(), 1)

        upload = serializer.save(user=self.user_premium)
        self.assertEqual(upload.images.count(), 3)

        upload = serializer.save(user=self.user_enterprise)
        self.assertEqual(upload.images.count(), 3)

    def test_image_upload_with_disallowed_extension(self):
        serializer = (
            self._create_image_upload_serializer(
                "example.pbm"
            )
        )

        self.assertEqual(serializer.is_valid(), False)

    def _upload_image(self, user_type):
        url = reverse("upload-list")
        example_image = SimpleUploadedFile(
            name="example.jpg",
            content=open("example.jpg", "rb").read(),
            content_type="image/jpeg",
        )
        data = {"image": example_image}

        self.client.force_authenticate(user=user_type)
        return self.client.post(url, data)

    def test_image_upload_view(self):
        response = self._upload_image(self.user_basic)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Upload.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 1)

    def test_temp_link_creation_view(self):
        self._upload_image(self.user_enterprise)

        url = reverse("templink-list")
        upload = Upload.objects.all()[0]
        data = {"upload": upload.id, "expiry_after": 300}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TempLink.objects.count(), 1)

    def test_valid_link_is_accessible(self):
        self._upload_image(self.user_enterprise)

        url = reverse("templink-list")
        upload = Upload.objects.all()[0]
        data = {"upload": upload.id, "expiry_after": 300}
        self.client.post(url, data)

        temp_link = TempLink.objects.all()[0]
        url = reverse("temporary-content", kwargs={"pk": temp_link.id})
        response = self.client.get(url)

        self.assertEqual(response.headers["Content-Type"], "image/jpg")

    def test_expired_link_is_not_accessible(self):
        self._upload_image(self.user_enterprise)

        url = reverse("templink-list")
        upload = Upload.objects.all()[0]
        data = {"upload": upload.id, "expiry_after": 300}
        self.client.post(url, data)

        temp_link = TempLink.objects.all()[0]
        freezer = freeze_time(timezone.now() + datetime.timedelta(seconds=500))
        freezer.start()
        url = reverse("temporary-content", kwargs={"pk": temp_link.id})
        response = self.client.get(url)
        freezer.stop()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
