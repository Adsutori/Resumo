from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .validators import validate_avatar_size
import random
import string

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

class UserManager(BaseUserManager):
    def create_user(self, email, nick, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is needed')
        if not nick:
            raise ValueError('Nick is needed')
        email = self.normalize_email(email)
        user = self.model(email=email, nick=nick, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nick, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, nick, password, **extra_fields)
    
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nick = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_avatar_size]
    )

    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(
        max_length=6,
        blank=True,
        default=generate_verification_code
    )
    verification_code_expires = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nick', 'first_name', 'last_name']

    objects = UserManager() 