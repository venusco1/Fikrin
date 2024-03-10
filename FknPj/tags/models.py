from django.db import models
from  Authentication.models import CustomUser




class Tag(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='tag_profile_pics', blank=True, null=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    likers = models.ManyToManyField(CustomUser,blank=True , related_name='liked_posts')
    # Add other fields as needed
