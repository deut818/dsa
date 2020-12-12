from django import forms
from phonenumber_field import formfields
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from djmoney.forms import MoneyField
from accounts.models import Member
from service.models import *
from shop.models import *
from orders.models import *
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Profile Picture"}))
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Full Name"}))
    role = forms.CharField(label='Role', widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Role"}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Email Address"}))
    tel = formfields.PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={"class": "form-control"}))
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Address"}))
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={"class":"form-control", "placeholder": "Date of Birth"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Password"}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Retype Password"}))

    class Meta:
        model = Member
        fields = ('picture', 'name', 'email', 'tel', 'role', 'address', 'date_of_birth', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Password"}))

class ClientForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label="Name")
    tel = formfields.PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Client
        fields = ['name', 'tel', 'email', 'address']

class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    ammount = MoneyField(max_digits=14, default_currency="UGX", decimal_places=0)
    quantity = forms.IntegerField(label="Quantity", widget=forms.NumberInput(attrs={"class": "form-control"}))
    discount = forms.IntegerField(label="Discount", widget=forms.NumberInput(attrs={"class": "form-control"}))
    paid = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-control"}))
    delivered = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-control"}))
    recieved = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-control"}))

    class Meta:
        model = Order
        exclude = ("client",)

class ServiceForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image = forms.FileField(widget=forms.FileInput(attrs={"class": "custom-file-input"}))
    available = forms.ChoiceField(widget=forms.CheckboxInput())

    class Meta:
        model = Service
        fields = ['title', 'image', 'available']

class ProjectForm(forms.ModelForm):
    INPROGRESS = "INPROGRESS"
    CANCELED = "CANCELED"
    PAUSED = "PAUSED"
    RESUMED = "RESUMED"
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    STATUS_CHOICES = [
        (INPROGRESS, 'In Progress'),
        (CANCELED, 'Canceled'),
        (PAUSED, "Paused"),
        (RESUMED, "Resumed"),
        (COMPLETED, "Completed"),
        (PENDING, "Pending")
    ]

    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    service = forms.ModelChoiceField(Service.objects.all())
    client = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    client_contact = formfields.PhoneNumberField(label="Contact", widget=PhoneNumberPrefixWidget(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"class": "form-control"}))
    budget = MoneyField(max_digits=14, default_currency="UGX", decimal_places=0)
    spent = MoneyField(max_digits=14, default_currency="UGX", decimal_places=0)
    duration = forms.DurationField(label="Duration", help_text="00:00:00")
    status = forms.ChoiceField(label="Status", widget=forms.Select(attrs={"class": "form-control"}), choices=STATUS_CHOICES)
    started = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control"}))
    ended = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control"}))


    class Meta:
        model = Project
        fields = ["title", "service", "client", "client_contact", "description", "budget", "spent", "duration", "status", "started", "ended"]

class ProjectFilesForm(forms.ModelForm):
    project = forms.ModelChoiceField(Project.objects.all())
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    file = forms.FileField(widget=forms.FileInput(attrs={"class": "custom-file-input"}))

    class Meta:
        model = ProjectFile
        fields = ["project", 'name', 'file']