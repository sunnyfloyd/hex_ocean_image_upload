from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from image_hoarder.images.models import Image, ThumbnailOption
from image_hoarder.images.serializers import ImageSerializer, ImageUploadSerializer
from image_hoarder.users.models import Plan, User
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile


class ImageTestCase(APITestCase):
    def setUp(self):
        # Create thumbnails
        tn200 = ThumbnailOption.objects.create(height=200)
        tn400 = ThumbnailOption.objects.create(height=400)

        # Create plans
        plan_basic = Plan.objects.create(
            name="Basic",
            keep_original=False,
            has_expiry_link=False
        )
        plan_basic.thumbnail_options.add(tn200)
        
        plan_premium = Plan.objects.create(
            name="Premium",
            keep_original=True,
            has_expiry_link=False
        )
        plan_premium.thumbnail_options.add(tn200, tn400)
        
        plan_enterprise = Plan.objects.create(
            name="Enterprise",
            keep_original=True,
            has_expiry_link=True
        )
        plan_enterprise.thumbnail_options.add(tn200, tn400)

        # Create users
        self.user_basic = User.objects.create(
            username='basic',
            password='123',
            plan=plan_basic
        )
        self.user_premium = User.objects.create(
            username='premium',
            password='123',
            plan=plan_premium
        )
        self.user_enterprise = User.objects.create(
            username='enterprise',
            password='123',
            plan=plan_enterprise
        )

    def test_me_now(self):
        example_image = SimpleUploadedFile(
            name='example.jpg',
            content=open('example.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        
        data = {
            "image": example_image
        }

        serializer = ImageUploadSerializer(data=data)
        serializer.is_valid()

        upload = serializer.save(user=self.user_basic)

