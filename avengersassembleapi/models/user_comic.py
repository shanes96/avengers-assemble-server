from django.db import models

class UserComic(models.Model):
    comic = models.ForeignKey("Comic", on_delete=models.CASCADE)
    user = models.ForeignKey("AvengerUser", on_delete=models.CASCADE)