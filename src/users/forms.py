from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from store.models import Customer
from django import forms

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=255, required=False)  # Champ d'adresse personnalisé
    phone_number = forms.CharField(max_length=15, required=False)  # Champ de numéro de téléphone personnalisé
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, required=True)  # Champ pour le type d'utilisateur

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'address', 'phone_number', 'user_type')  # Inclure le champ user_type

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # Appliquer la classe Bootstrap

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.user_type = self.cleaned_data['user_type']  # Assurez-vous de définir le type d'utilisateur
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))


class CustomSetPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='Nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmer le nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
