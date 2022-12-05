from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractBaseUser, UserManager


class AvengerUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=50, null=True, blank=True) 
    favorite_comics = models.CharField(null=True, blank=True, max_length=100)
    favorite_movies = models.CharField(null=True, blank=True, max_length=100)


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'