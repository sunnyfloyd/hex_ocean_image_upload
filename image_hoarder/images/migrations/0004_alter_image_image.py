# Generated by Django 3.2.9 on 2021-11-11 19:08

from django.db import migrations, models
import image_hoarder.images.models
import image_hoarder.images.validators


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_image_expiry_after'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=image_hoarder.images.models.get_file_path, validators=[image_hoarder.images.validators.validate_image_extension]),
        ),
    ]
