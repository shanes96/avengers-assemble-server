from django.db import models

class BattleRequests(models.Model):
    opponent_1 = models.ForeignKey("AvengerUser", on_delete=models.CASCADE, related_name="opponent_1")
    opponent_2 = models.ForeignKey("AvengerUser", on_delete=models.CASCADE, related_name="opponent_2")
