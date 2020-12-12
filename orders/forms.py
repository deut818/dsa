from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'quantity', 'amount', 'paid', 'delivered', 'recieved']
