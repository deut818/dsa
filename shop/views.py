from shop.recommender import Recommender
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.models import Category, Product
from cart.forms import CartAddProductForm
from shop.forms import ContactForm
from django.core.mail import send_mail

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    sort_10 = Product.objects.filter(available=True)[:10]
    sort_25 = Product.objects.filter(available=True)[:25]
    sort_50 = Product.objects.filter(available=True)[:50]
    sort_100 = Product.objects.filter(available=True)[:100]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products, 'cart_product_form': cart_product_form})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form, 'recommended_products':recommended_products, 'sort_10':sort_10, 'sort_25':sort_25, 'sort_50':sort_50, 'sort_100':sort_100})

