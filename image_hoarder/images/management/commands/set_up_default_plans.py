from django.core.management.base import BaseCommand
from image_hoarder.images.models import ThumbnailOption
from image_hoarder.users.models import User, Plan


class Command(BaseCommand):
    help = "Sets up a default plans and thumbnail options."

    def handle(self, *args, **options):
        try:
            User.objects.get(username="admin")

        except User.DoesNotExist:
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
            User.objects.create_superuser(
                username="admin", password="123", plan=plan_enterprise
            )

            User.objects.create_user(username="basic", password="123", plan=plan_basic)
            User.objects.create_user(
                username="premium", password="123", plan=plan_premium
            )
            User.objects.create_user(
                username="enterprise", password="123", plan=plan_enterprise
            )

            self.stdout.write(
                self.style.SUCCESS("Default plans have been successfully created.")
            )
