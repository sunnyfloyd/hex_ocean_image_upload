from django.contrib import admin
from .models import ThumbnailOption, Image


@admin.register(ThumbnailOption)
class ThumbnailAdmin(admin.ModelAdmin):
    pass
    

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
