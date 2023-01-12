from django.db import models

class CharacterTeam(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    team = models.ForeignKey("UserTeam", on_delete=models.CASCADE)