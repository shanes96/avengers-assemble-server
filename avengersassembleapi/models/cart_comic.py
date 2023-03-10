from django.db import models

class CartComic(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    comic = models.ForeignKey("Comic", on_delete=models.CASCADE, to_field="comic_id")
    quantity = models.PositiveIntegerField(default=1)