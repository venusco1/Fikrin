from django.contrib import admin

from .models import CustomUser, GalleryImage


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "profile_pic", "mobile_number")


admin.site.register(CustomUser)


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("description", "image")


admin.site.register(GalleryImage)
