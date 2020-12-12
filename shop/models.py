from django.utils.translation import gettext_lazy as _
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField

from service.models import *


class Category(models.Model):
    service = models.ForeignKey(Service, related_name="categories", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    image = models.FileField(upload_to="categories/%Y/%m/%d", blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
# 
    # def get_num_products(self):
    #     return int(self.products.count())

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.FileField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = MoneyField(max_digits=14, default_currency="UGX", decimal_places=0, null=True)
    available = models.BooleanField(default=True)
    color = models.CharField(max_length=255, blank=True, default="Red")
    size = models.CharField(max_length=255, blank=True, default="XL")
    brand = models.CharField(max_length=255, blank=True, default="DSG")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Stock(models.Model):
    product = models.ForeignKey(Product, related_name="stock", on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=0, default_currency="UGX", null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    initial = models.DecimalField(max_digits=10, decimal_places=1)

    

    