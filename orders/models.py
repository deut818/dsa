from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                            MaxValueValidator
from coupons.models import Coupon
from shop.models import Product
from service.models import *


class Order(models.Model):
    client = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, default_currency="UGX", decimal_places=0, null=True)
    paid = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    delivered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'Order {} by {}'.format(self.id, self.client)

