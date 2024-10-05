from django.conf import settings
import logging
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from .forms import *
from store.models import Customer, Product  # Assurez-vous d'importer vos modèles
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from store.forms import *
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm
from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Inscription réussie. Veuillez vous connecter.")
            phone_number = user.phone_number

            # Essayer d'envoyer le SMS, gérer l'erreur si nécessaire
            try:
                send_confirmation_sms(phone_number)
            except Exception as e:
                messages.error(request, "Une erreur s'est produite lors de l'envoi du SMS. Veuillez réessayer.")
                logging.error(f"Erreur lors de l'envoi du SMS: {e}")

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def send_confirmation_sms(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body="Bienvenue! Votre inscription a été réussie.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
    except TwilioRestException as e:
        logging.error(f"Erreur Twilio: {e}")
        raise Exception(f"Erreur lors de l'envoi du SMS: {e}")


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirection en fonction du type d'utilisateur
            if user.user_type == 'seller':
                return redirect('seller_dashboard')  # Redirigez vers le tableau de bord du vendeur
            else:
                return redirect('client_dashboard')  # Redirigez vers le tableau de bord du client
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def custom_password_reset_request(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                subject = 'Réinitialisation de votre mot de passe'
                email_template_name = 'users/password_reset_email.html'
                domain = request.get_host()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                context = {
                    'email': user.email,
                    'domain': domain,
                    'site_name': 'ecommerce',
                    'uidb64': uidb64,
                    'token': token,
                    'protocol': 'http',
                }

                email_message = render_to_string(email_template_name, context)

                try:
                    send_mail(
                        subject,
                        email_message,
                        settings.EMAIL_HOST_USER,  # Utiliser l'adresse e-mail configurée
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, "Veuillez consulter votre adresse e-mail pour réinitialiser votre mot de passe.")
                    return redirect('password_reset_done')  # Rediriger vers une page de confirmation
                except Exception as e:
                    form.add_error(None, "Une erreur s'est produite lors de l'envoi de l'e-mail. Veuillez réessayer.")
                    logging.error(f"Erreur d'envoi d'email: {e}")
            else:
                form.add_error('email', "Aucun compte associé à cette adresse e-mail.")
    else:
        form = CustomPasswordResetForm()

    return render(request, 'users/password_reset_form.html', {'form': form})

def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')

def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == "POST":
        form = CustomSetPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['new_password1']
            password2 = form.cleaned_data['new_password2']
            if password1 == password2:
                user.set_password(password1)
                user.save()
                login(request, user)  # Connectez l'utilisateur après le changement de mot de passe
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
                return redirect('password_reset_complete')
    else:
        form = CustomSetPasswordForm()
    return render(request, 'users/password_reset_confirm.html', {'form': form, 'validlink': user is not None})

def custom_password_reset_complete(request):
    return render(request, 'users/password_reset_complete.html')

@login_required
def user_profile(request):
    user = request.user  # Récupérer l'utilisateur connecté
    try:
        customer = Customer.objects.get(user=user)  # Récupérer le profil client
    except Customer.DoesNotExist:
        customer = None  # Gérer le cas où l'utilisateur n'est pas un client

    return render(request, 'users/profile.html', {'user': user, 'customer': customer})

@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)  # Récupérer les produits du vendeur
    form = ProductForm()  # Créer une instance du formulaire

    return render(request, 'users/seller/seller_dashboard.html', {
        'products': products,
        'form': form,  # Passer le formulaire au template
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Inclure request.FILES pour les images
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Associe le produit à l'utilisateur connecté
            product.save()
            return redirect('store')  # Redirige vers la page de la boutique ou vers un tableau de bord
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})
@login_required
def authorize_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_authorized = True
    product.save()
    messages.success(request, "Produit autorisé avec succès.")
    return redirect('seller_dashboard')  # Rediriger vers le tableau de bord du vendeur

@login_required
def client_dashboard(request):
    # Récupérer les produits qui sont autorisés
    products = Product.objects.filter(is_authorized=True)
    return render(request, 'users/client/client_dashboard.html', {'products': products})
@login_required
def customer_list(request):
    customers = Customer.objects.all()  # Récupérer tous les clients
    return render(request, 'users/customer_list.html', {'customers': customers})
