# ecommerce/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Ajoute les URLs de l'application store
    path('users/', include('users.urls')),  # Ajoute les URLs de l'application users
]
