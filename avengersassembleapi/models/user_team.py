from django.db import models

class UserTeam(models.Model):
    user = models.ForeignKey('AvengerUser', on_delete=models.CASCADE, related_name="user_team")
    characters = models.ManyToManyField('Character', through='CharacterTeam')
    team_name= models.CharField(max_length=155)