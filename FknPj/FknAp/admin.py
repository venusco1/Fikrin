from django.contrib import admin
from . models import *


# admin.site.register(CustomUser)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'profile_pic', 'bio', 'cover', 'mobile_number', 'mobile_visible')

admin.site.register( CustomUser)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('creater', 'date_created', 'content_text', 'comment_count')
    list_filter = ('date_created', 'comment_count')
    search_fields = ('creater', 'content_text')
    readonly_fields = ('date_created', 'comment_count')

""" Username: nzmdn
Email address: nzmdn@gmail.com
Password: nzmdn """