from .models import Category, Product
from django.shortcuts import redirect, get_object_or_404

def cat_obj(request, *args, **kwargs):
    cat_obj = Category.objects.all()
    return {'cat_obj':cat_obj}

