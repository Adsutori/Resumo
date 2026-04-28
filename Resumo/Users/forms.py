from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


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


User = get_user_model()


class ChangeNickForm(forms.Form):
    nick = forms.CharField(
        max_length=50,
        label='Nowy nick',
        widget=forms.TextInput(attrs={'placeholder': 'Twój nowy nick'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_nick(self):
        nick = self.cleaned_data['nick'].strip()
        if User.objects.filter(nick=nick).exclude(pk=self.user.pk).exists():
            raise ValidationError('Ten nick jest już zajęty.')
        return nick


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        label='Nowy adres e-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'nowy@email.com'}),
    )
    password = forms.CharField(
        label='Aktualne hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Potwierdź hasłem'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError('Ten adres e-mail jest już używany.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise ValidationError('Nieprawidłowe hasło.')
        return password


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Aktualne hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Aktualne hasło'}),
    )
    new_password = forms.CharField(
        label='Nowe hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło (min. 8 znaków)'}),
    )
    confirm_password = forms.CharField(
        label='Powtórz nowe hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        password = self.cleaned_data['current_password']
        if not self.user.check_password(password):
            raise ValidationError('Nieprawidłowe aktualne hasło.')
        return password

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise ValidationError({'confirm_password': 'Hasła nie są identyczne.'})
        if p1:
            try:
                validate_password(p1, self.user)
            except ValidationError as e:
                raise ValidationError({'new_password': e.messages})
        return cleaned


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Max 5MB
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError('Plik jest za duży. Maksymalny rozmiar to 5 MB.')
            # Tylko obrazy
            allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
            if hasattr(avatar, 'content_type') and avatar.content_type not in allowed:
                raise ValidationError('Dozwolone formaty: JPG, PNG, WEBP, GIF.')
        return avatar


class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Wpisz hasło aby potwierdzić'}),
    )
    confirm = forms.BooleanField(
        label='Rozumiem, że tej operacji nie można cofnąć.',
        required=True,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise ValidationError('Nieprawidłowe hasło.')
        return password
