from django.db import models

class Cart(models.Model):
    user = models.ForeignKey("AvengerUser", on_delete=models.CASCADE)
    comics = models.ManyToManyField("Comic", through='CartComic')