from django.urls import path, re_path
from .views import CartListView, CartRudView, RegisterAPI, OrderRudView, ProductRudView, CategoryListView,ProductListByCategoryView, ProductListView, OrderListView, UserCreateAPIView, UserListAPIView

urlpatterns = [
    re_path('order/(?P<pk>\d+)/', OrderRudView.as_view(), name='order_api'),
    re_path('product/(?P<pk>\d+)/', ProductRudView.as_view(), name='product_api'),  
    path('products/', ProductListView.as_view(), name='products_list_api'),
    re_path('cart/(?P<pk>\d+)/', CartRudView.as_view(), name='cart_api'),
    path('categories/', CategoryListView.as_view(), name='category_list_api'),
    path('orders/', OrderListView.as_view(), name='orders_list_api'),
    path('users/', UserListAPIView.as_view(), name='user_create_api'),
    path('users/create/', UserCreateAPIView.as_view(), name='user_create_api'),
    path('user/register/', RegisterAPI.as_view(), name="user_register"),
]
