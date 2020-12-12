from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Third Party imports
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField

class MemberManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=99, blank=True)
    salary = MoneyField(max_digits=14, decimal_places=2, default_currency='UGX', null=True, blank=True)
    allowance = MoneyField(max_digits=14, decimal_places=2, default_currency='UGX', null=True, blank=True)
    picture = models.ImageField(upload_to='pictures/%Y/%m/%d/', blank=True, default="https://i.dlpng.com/statpreview.png")
    address = models.TextField(blank=True)
    tel = PhoneNumberField(blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_valid =  models.BooleanField(default=True)
    is_resigned = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin