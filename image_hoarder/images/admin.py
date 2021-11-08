from django.contrib import admin
from .models import Thumbnail, Image


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    pass
    

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
