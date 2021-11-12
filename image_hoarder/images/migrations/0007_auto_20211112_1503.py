# Generated by Django 3.2.9 on 2021-11-12 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_remove_image_expiry_after'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templink',
            name='image',
        ),
        migrations.AddField(
            model_name='templink',
            name='upload',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='temp_links', to='images.upload'),
            preserve_default=False,
        ),
    ]
