
from django.contrib import admin
from .models import Tag, Post

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile_picture')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'display_tags')

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
