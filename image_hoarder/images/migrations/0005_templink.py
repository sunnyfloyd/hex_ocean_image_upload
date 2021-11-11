# Generated by Django 3.2.9 on 2021-11-11 20:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_alter_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempLink',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiry_after', models.IntegerField(default=None, null=True, validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)])),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_links', to='images.image')),
            ],
        ),
    ]