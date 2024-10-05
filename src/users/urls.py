from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),  # URL pour l'enregistrement des utilisateurs
    path('login/', user_login, name='login'),  # URL pour la connexion des utilisateurs
    path('logout/', auth_views.LogoutView.as_view(next_page='store'), name='logout'),  # URL pour la déconnexion
    path('profile/', user_profile, name='profile'),  # URL pour le profil de l'utilisateur
    path('reset_password/', custom_password_reset_request, name='password_reset'),  # URL pour demander la réinitialisation de mot de passe
    path('reset_password_confirm/<uidb64>/<token>/', custom_password_reset_confirm, name='password_reset_confirm'),  # URL pour confirmer la réinitialisation de mot de passe
    path('reset_password_complete/', custom_password_reset_complete, name='password_reset_complete'),  # URL pour finaliser la réinitialisation de mot de passe
    path('customers/', customer_list, name='customer_list'),  # URL pour la liste des clients
    path('reset_password/done/', password_reset_done, name='password_reset_done'),  # URL pour la page après réinitialisation de mot de passe
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard'),  # URL pour le tableau de bord des vendeurs
    path('add_product/', add_product, name='add_product'),  # URL pour ajouter un produit
    path('authorize_product/<int:product_id>/', authorize_product, name='authorize_product'),  # URL pour autoriser un produit
    path('client_dashboard/', client_dashboard, name='client_dashboard'),  # URL pour le tableau de bord des clients
]
