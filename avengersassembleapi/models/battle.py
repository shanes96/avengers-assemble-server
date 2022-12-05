from django.db import models

class Battle(models.Model):
    team_1 = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="user_team_1")
    team_2 = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="user_team_2")