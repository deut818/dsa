from django.db import models
from djmoney.models.fields import MoneyField
from accounts.models import Member
from django.shortcuts import reverse
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField
from filer.fields.file import FilerFileField
# Create your models here

class Client(models.Model):
    name = models.CharField(max_length=255, blank=True)
    tel = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="images/services/", blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('main:service_detail', args=[self.id])

class Project(models.Model):
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

    service = models.ForeignKey(Service, related_name="projects", on_delete=models.CASCADE)
    client = models.CharField(max_length=255, blank=True)
    client_contact = PhoneNumberField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = MoneyField(max_digits=14, decimal_places=2, default_currency='UGX', null=True)
    spent = MoneyField(max_digits=14, decimal_places=2, default_currency='UGX', null=True)
    duration = models.DurationField()
    started = models.DateField()
    ended = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.title

    def get_total_spent(self):
        return sum(Decimal(self.spent) for item in self.objects.all())
    
    def get_absolute_url(self):
        return reverse('main:project_detail', args=[self.id])

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, related_name="files", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="projects/")
    extension = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

