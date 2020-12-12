from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from shop.models import Category, Product, Cart
from orders.models import Order
from knox.models import AuthToken
from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework import permissions
from .serializers import CartSerializer, OrderSerializer, ProductSerializer, CategorySerializer, UserSerializer, RegistrationSerializer

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserCreateAPIView(generics.CreateAPIView):
     serializer_class = UserSerializer
     queryset = User.objects.all()
     permission_classes = [permissions.AllowAny]

     def post(self, request, *args, **kwargs):
          return super().post(request, *args, **kwargs)

class UserListAPIView(generics.ListAPIView):
     serializer_class = UserSerializer
     queryset = User.objects.all()
     permission_classes = [permissions.AllowAny]

class CategoryListView(generics.ListAPIView):
     # q1 = Category.objects.annotate(numy=Count('products'))
     q2 = Category.objects.all()
     permission_classes = [permissions.AllowAny]
     serializer_class = CategorySerializer
     queryset = q2

class ProductRudView(generics.RetrieveAPIView):
     lookup_field = 'pk'
     permission_classes = [permissions.AllowAny]
     serializer_class = ProductSerializer
     queryset = Product.objects.all()

class OrderRudView(generics.RetrieveUpdateDestroyAPIView):
     lookup_field = 'pk'
     permission_classes = [permissions.AllowAny]
     serializer_class = OrderSerializer
     queryset = Order.objects.all()

class CartRudView(generics.RetrieveUpdateDestroyAPIView):
     lookup_field = 'pk'
     permission_classes = [permissions.AllowAny]
     serializer_class = CartSerializer
     queryset = Cart.objects.all()

class ProductListView(generics.ListAPIView):
     serializer_class = ProductSerializer
     permission_classes = [permissions.AllowAny]
     queryset = Product.objects.all()

class CartListView(generics.ListAPIView):
     serializer_class = CartSerializer
     permission_classes = [permissions.AllowAny]
     queryset = Cart.objects.all()

class ProductListByCategoryView(generics.ListAPIView):
     lookup_field = 'category'
     serializer_class = ProductSerializer
     permission_classes = [permissions.AllowAny]

class OrderListView(generics.ListAPIView):
     serializer_class = OrderSerializer
     permission_classes = [permissions.AllowAny]
     queryset = Order.objects.filter()
