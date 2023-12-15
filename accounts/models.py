from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
