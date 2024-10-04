# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('visitor', 'Visitor'),
    ]
    phone_number = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')  # User type field
    customer = models.OneToOneField('store.Customer', on_delete=models.CASCADE, null=True, blank=True, related_name='user_customer')

    def __str__(self):
        return self.username
