from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm)
from django.contrib.auth.models import User


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'votre@email.com'
        }))

    class Meta:
        model  = User
        fields = ['username', 'email',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les placeholders
        self.fields['username'].widget.attrs\
            .update({'placeholder': 'Nom utilisateur'})
        self.fields['password1'].widget.attrs\
            .update({'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs\
            .update({'placeholder': 'Confirmer mot de passe'})


class ConnexionForm(AuthenticationForm):
    """Formulaire de connexion"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs\
            .update({'placeholder': 'Nom utilisateur'})
        self.fields['password'].widget.attrs\
            .update({'placeholder': 'Mot de passe'})