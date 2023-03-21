from django.db import models
import decimal

class CartComic(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    comic = models.ForeignKey("Comic", on_delete=models.CASCADE, to_field="comic_id")
    quantity = models.PositiveIntegerField(default=1)

    def comic_sub_total(self):
        return self.quantity * self.comic.comic_price 
    
    @property
    def cart_sub_total(self):
        total = sum(item.comic_sub_total() for item in self.cart.cartcomic_set.all())
        return '${:.2f}'.format(total)

    @property
    def cart_total(self):
        sub_total = sum(item.comic_sub_total() for item in self.cart.cartcomic_set.all())
        tax = decimal.Decimal('0.06') * sub_total
        total = sub_total + tax
        return '${:.2f}'.format(total.quantize(decimal.Decimal('.01')))


        

    @property
    def tax(self):
        sub_total = sum(item.comic_sub_total() for item in self.cart.cartcomic_set.all())
        tax_amount = sub_total * decimal.Decimal('0.06')
        return '${:.2f}'.format(tax_amount.quantize(decimal.Decimal('.01')))

        