from django.conf import settings
import logging
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils.http import  urlsafe_base64_decode
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm
from store.models import Customer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .forms import CustomPasswordResetForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 'customer':
                Customer.objects.create(user=user, name=user.username, email=form.cleaned_data['email'])
            login(request, user)
            return redirect('store')  # Rediriger vers la page d'accueil
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('store')  # Rediriger vers la page d'accueil
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
                except Exception as e:
                    form.add_error(None, "Une erreur s'est produite lors de l'envoi de l'e-mail. Veuillez réessayer.")
                    logging.error(f"Erreur d'envoi d'email: {e}")

                # Rediriger vers l'URL de confirmation avec uidb64 et token
                return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
            else:
                form.add_error('email', "Aucun compte associé à cette adresse e-mail.")
    else:
        form = CustomPasswordResetForm()

    return render(request, 'users/password_reset_form.html', {'form': form})
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
                return redirect('password_reset_complete')
    else:
        form = CustomSetPasswordForm()
    return render(request, 'users/password_reset_confirm.html', {'form': form, 'validlink': user is not None})

def custom_password_reset_complete(request):
    return render(request, 'users/password_reset_complete.html')

@login_required
def customer_list(request):
    customers = Customer.objects.all()  # Récupérer tous les clients
    return render(request, 'users/customer_list.html', {'customers': customers})
