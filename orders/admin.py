from django.contrib import admin

from .models import Order
import csv
import datetime
from django.http import HttpResponse

from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'product', 'amount', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
