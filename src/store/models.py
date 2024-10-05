from django.conf import settings
from django.db import models


# Modèle Client
class Customer(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='customer_user')  # Link to CustomUser
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255, null=True, blank=True)  # Ajout du champ d'adresse
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Ajout du champ de numéro de téléphone

    def __str__(self):
        return self.name

# Modèle Produit
class Product(models.Model):
    is_authorized = models.BooleanField(default=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # Champs supplémentaires
    description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# Modèle Commande
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    # Champ de statut pour suivre l'état de la commande
    STATUS_CHOICES = (
        ('Pending', 'En attente'),
        ('Shipped', 'Expédiée'),
        ('Delivered', 'Livrée'),
        ('Cancelled', 'Annulée'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return sum([oi.quantity for oi in orderitems])

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        return sum([oi.get_total for oi in orderitems])

# Modèle Article de Commande
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

# Modèle Adresse de Livraison
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=15, null=False)  # Ajout du numéro de téléphone
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
