
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.TextField(max_length=160, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    mobile_visible = models.BooleanField(default=True)


    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


class Post(models.Model):
    creater = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True)
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField()
    likers = models.ManyToManyField(CustomUser,blank=True , related_name='likes')
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"
   
    def edit_post(self, new_text):
        self.content_text = new_text
        self.save()

    def append(self, name, value):
        self.name = value





