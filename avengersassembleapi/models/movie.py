from django.db import models

class Movie(models.Model):
    movie_id=models.IntegerField(null=True)
    movie_title= models.CharField(max_length=155)
    movie_picture=models.CharField(max_length=500)