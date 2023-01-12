from django.db import models

class Character(models.Model):
    character_id=models.IntegerField(null=True)
    character_name= models.CharField(max_length=155)
    character_picture=models.CharField(max_length=500)
    character_extension=models.CharField(max_length=500)