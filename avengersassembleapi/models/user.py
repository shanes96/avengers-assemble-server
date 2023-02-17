from django.db import models
from django.contrib.auth.models import User

class AvengerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, null=True, blank=True)
    # profile_image = models.ImageField(upload_to='media', null=True, blank=True) 
    profile_image = models.CharField(max_length=50, null=True, blank=True) 
    favorite_comics = models.ManyToManyField('Comic',through="UserComic")
    favorite_movies = models.ManyToManyField('Movie',through="UserMovie")
    user_wins = models.IntegerField(null=True)
    user_losses = models.IntegerField(null=True)
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'