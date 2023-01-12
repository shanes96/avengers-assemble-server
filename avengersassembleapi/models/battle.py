from django.db import models

class Battle(models.Model):
    team_1 = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="team_1")
    team_2 = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="team_2", null=True)
    user_being_challenged = models.ForeignKey("AvengerUser", on_delete=models.CASCADE, related_name="user_being_challenged", null=True)
    number_of_votes_team_1 = models.IntegerField(default=0)
    number_of_votes_team_2 = models.IntegerField(default=0)
    winner = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="battle_winner", null=True)
    loser = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="battle_loser", null=True)