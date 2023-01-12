from django.db import models

class UserMovie(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    user = models.ForeignKey("AvengerUser", on_delete=models.CASCADE)