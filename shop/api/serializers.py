from rest_framework import serializers
from shop.models import Category, Product, Cart
from orders.models import Order
from django.contrib.auth.models import User
from django.db.models import Count

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ('id', 'first_name', 'last_name', 'username', 'email')

class RegistrationSerializer(serializers.ModelSerializer):
     password2 = serializers.CharField(style={'input-type': 'password'}, write_only=True)

     class Meta:
          model = User
          fields = ["username", "email", "first_name", "last_name", "password", "password2"]
          extra_kwargs = {
               'password': {'write_only': True}
          }
     def save(self):
          user = User(
               email=self.validated_data['email'],
               username=self.validated_data['username'],
          )
          password = self.validated_data['password']
          password2 = self.validated_data['password2']
          first_name = self.validated_data['first_name']
          last_name = self.validated_data['last_name']

          if password != password2:
               raise serializers.ValidationError({'password': 'Passwords must match.'})
          user.set_password(password)
          user.first_name = first_name
          user.last_name = last_name
          user.save()
          return user

class CategorySerializer(serializers.ModelSerializer):
     # products = Category.objects.annotate(Count('products'))
     class Meta:
          model = Category
          fields = ["id", "name", 'image', "slug", "products"]
class ProductSerializer(serializers.ModelSerializer):
     class Meta:
          model = Product
          fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
     class Meta:
          model = Cart
          fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
     class Meta:
          model = Order
          fields = "__all__"
