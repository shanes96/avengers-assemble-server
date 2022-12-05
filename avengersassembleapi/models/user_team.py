from django.db import models

class UserTeam(models.Model):
    name = models.CharField(max_length=155)
    user = models.ForeignKey("AvengerUser", on_delete=models.CASCADE, related_name="user_team")