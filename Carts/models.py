from django.db import models
from Store.models import Product
from Accounts.models import *
from Store.models import Size

from django.db import models
from Accounts.models import Account
from Store.models import Product, Size

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product)

    # ✅ Update subtotal automatically
    def save(self, *args, **kwargs):
        self.sub_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
