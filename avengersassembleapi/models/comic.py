from django.db import models

class Comic(models.Model):
    comic_id=models.IntegerField(null=True)
    comic_title= models.CharField(max_length=155)
    comic_picture=models.CharField(max_length=500)
    comic_extension=models.CharField(max_length=500)