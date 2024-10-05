from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('client', 'Client'),
        ('seller', 'Seller'),
    ]
    phone_number = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')  # Champ de type d'utilisateur
    customer = models.OneToOneField('store.Customer', on_delete=models.CASCADE, null=True, blank=True, related_name='user_customer')

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')  # Lien vers l'utilisateur
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.name
