from django.db.models import Count
from django import template
from ..models import Post
from shop.models import Product
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from dsg.forms import SearchForm

register = template.Library()

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag('search.html')
def dsg_search(request):
    search_form = SearchForm()
    query = None
    users_results = []
    post_results = []
    product_results = []
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            posts = Post.objects.all()
            products = Product.objects.all()
            users = User.objects.filter(profile__member=True)
            post_results = posts.annotate(search=SearchVector('title', 'body'),).filter(search=query)
            product_results = products.annotate(search=SearchVector('name', 'description'),).filter(search=query)
            users_results = users.annotate(search=SearchVector('username', 'email', 'first_name', 'last_name'),).filter(search=query)
    return {'search_form': search_form, 'query':query, 'user_results':users_results, 'post_results':post_results, 'product_results':product_results}
