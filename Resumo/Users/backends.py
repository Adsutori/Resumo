from django.contrib.auth.backends import ModelBackend
from django.contrib.auth          import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authenticates using email + password instead of username + password.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 'username' param is reused by Django internals — here it carries email
        email = username
        if not email:
            return None

        try:
            user = User.objects.get(email=email.lower().strip())
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
