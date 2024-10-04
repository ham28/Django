# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),  # Page principale de la boutique
    path('cart/', views.cart, name="cart"),  # Page du panier
    path('checkout/', views.checkout, name="checkout"),  # Page de paiement
    path('update_item/', views.updateItem, name="update_item"),  # Mise à jour de l'article
]
