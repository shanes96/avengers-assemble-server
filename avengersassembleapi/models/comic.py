from django.db import models

class Comic(models.Model):
    comic_id=models.IntegerField(unique=True, null=True)
    comic_title= models.CharField(max_length=155)
    comic_picture=models.CharField(max_length=500)
    comic_extension=models.CharField(max_length=500)
    quantity = models.PositiveIntegerField(default=1)
    comic_price = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)