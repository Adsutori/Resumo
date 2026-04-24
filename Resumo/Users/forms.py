from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'twoj@email.com',
            'autocomplete': 'email',
        })
    )
    nick = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'jankowalski99',
            'autocomplete': 'username',
        })
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Jan'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Kowalski'})
    )

    terms = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'Musisz zaakceptować Regulamin i Politykę prywatności.'
        }
    )

    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name',
            'nick', 'email',
            'password1', 'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Konto z tym adresem e-mail już istnieje.')
        return email

    def clean_nick(self):
        nick = self.cleaned_data.get('nick', '').strip()
        if User.objects.filter(nick__iexact=nick).exists():
            raise forms.ValidationError('Ten nick jest już zajęty.')
        return nick


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'twoj@email.com',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(required=False)


class VerifyEmailForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': '123456',
            'autocomplete': 'one-time-code',
            'inputmode':    'numeric',
            'pattern':      '[0-9]{6}',
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if not code.isdigit():
            raise forms.ValidationError('Kod musi składać się z 6 cyfr.')
        return code


class ResendVerificationForm(forms.Form):
    email = forms.EmailField()
