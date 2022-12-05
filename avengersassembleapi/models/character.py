from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=155)
    team = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="character_user_team")