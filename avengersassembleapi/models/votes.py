from django.db import models

class Votes(models.Model):
    user = models.ForeignKey("AvengerUser", on_delete=models.CASCADE, related_name="vote_user_id")
    battle = models.ForeignKey("Battle", on_delete=models.CASCADE, related_name="battle")
    user_team = models.ForeignKey("UserTeam", on_delete=models.CASCADE, related_name="_vote_user_team")