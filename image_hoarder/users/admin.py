from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Plan


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


UserAdmin.list_display += ("plan",)
UserAdmin.list_filter += ("plan",)
UserAdmin.fieldsets += (("User Plan", {"fields": ("plan",)}),)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass
