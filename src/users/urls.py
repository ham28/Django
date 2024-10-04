# users/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('reset_password/', custom_password_reset_request, name='password_reset'),
    path('reset_password_confirm/<uidb64>/<token>/', custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_complete/', custom_password_reset_complete, name='password_reset_complete'),
    path('customers/', customer_list, name='customer_list'),
    path('reset_password/done/', password_reset_done, name='password_reset_done'),
]
