from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import Member

from djmoney.forms.fields import MoneyField
from djmoney.forms import widgets as money
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field import widgets


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    picture = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={"class":"form-control"}))
    role = forms.CharField(label='Role', widget=forms.TextInput(attrs={"class":"form-control"}))
    tel = PhoneNumberField()
    salary = MoneyField(max_digits=19, decimal_places=0, default_currency='UGX')
    allowance = MoneyField(max_digits=19, decimal_places=0, default_currency='UGX')
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={"class":"form-control"}))

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


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    picture = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    tel = PhoneNumberField()
    salary = MoneyField(max_digits=19, decimal_places=0, default_currency='UGX')
    allowance = MoneyField(max_digits=19, decimal_places=0, default_currency='UGX')
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={"class":"form-control"}))
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = ('picture', 'name', 'tel', 'role', 'salary', 'allowance', 'address', 'email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'tel', 'role', 'salary', 'allowance', 'address', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('picture', 'name', 'tel', 'role', 'salary', 'allowance', 'address', 'email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Member, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)