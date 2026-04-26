from django.shortcuts               import render, redirect
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.utils                   import timezone
from django.views.decorators.http   import require_POST
from datetime import datetime


from .forms   import RegisterForm, LoginForm, VerifyEmailForm, ResendVerificationForm
from .utils   import send_verification_email
from django.contrib.auth import get_user_model
User = get_user_model()

# ================================================================
# REGISTER
# ================================================================
def register_view(request):
    """
    GET  — show empty registration form
    POST — validate, create inactive user, send verification email
    """
    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Save user but keep inactive until email is verified
            user = form.save(commit=False)
            user.is_active   = False   # can't log in until verified
            user.is_verified = False
            user.save()

            # Send 6-digit code
            send_verification_email(user)

            # Store email in session so verify page knows who to verify
            request.session['pending_verification_email'] = user.email

            messages.success(
                request,
                f'Konto zostało utworzone! Sprawdź skrzynkę {user.email}.'
            )
            return redirect('users:verify_email')
        else:
            messages.error(request, 'Popraw błędy w formularzu.')

    return render(request, 'users/register.html', {'form': form})


# ================================================================
# LOGIN
# ================================================================
def login_view(request):
    """
    GET  — show login form
    POST — authenticate, check verification, log in
    """
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email       = form.cleaned_data['email'].lower().strip()
            password    = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            user = authenticate(request, username=email, password=password)

            if user is None:
                # Check if user exists but is not active (unverified)
                try:
                    unverified = User.objects.get(email=email)
                    if not unverified.is_active:
                        request.session['pending_verification_email'] = email
                        messages.warning(
                            request,
                            'Twoje konto nie zostało jeszcze zweryfikowane. '
                            'Sprawdź skrzynkę e-mail lub wyślij kod ponownie.'
                        )
                        return redirect('users:verify_email')
                except User.DoesNotExist:
                    pass

                messages.error(request, 'Nieprawidłowy e-mail lub hasło.')

            else:
                # Session expiry: 0 = browser session, else 2 weeks
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(60 * 60 * 24 * 14)

                login(request, user)


                # Respect ?next= redirect param
                next_url = request.GET.get('next') or 'dashboard:dashboard'
                return redirect(next_url)

    return render(request, 'users/login.html', {'form': form})


# ================================================================
# LOGOUT
# ================================================================
@require_POST
def logout_view(request):
    """
    POST only — logs out and redirects to home.
    POST-only prevents CSRF logout attacks.
    """
    logout(request)
    return redirect('/')


# ================================================================
# VERIFY EMAIL
# ================================================================
def verify_email_view(request):
    """
    GET  — show verify page (reads email from session)
    POST — validate 6-digit code, activate account, log in
    """
    email = request.session.get('pending_verification_email')

    # If no email in session and user is already verified → dashboard
    if not email and request.user.is_authenticated and request.user.is_verified:
        return redirect('dashboard:dashboard')

    # If no email in session at all → send to register
    if not email:
        messages.error(request, 'Sesja wygasła. Zarejestruj się ponownie.')
        return redirect('users:register')

    form = VerifyEmailForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            code = form.cleaned_data['code']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Nie znaleziono konta. Zarejestruj się ponownie.')
                return redirect('users:register')

            # Check expiry
            if user.verification_code_expires and timezone.now() > user.verification_code_expires:
                messages.error(
                    request,
                    'Kod wygasł. Wyślij nowy kod poniżej.'
                )
                return render(request, 'users/verify_email.html', {
                    'form':  form,
                    'email': email,
                })

            # Check code match
            if user.verification_code != code:
                messages.error(request, 'Nieprawidłowy kod weryfikacyjny.')
                return render(request, 'users/verify_email.html', {
                    'form':  form,
                    'email': email,
                })

            # ✅ All good — activate user
            user.is_active   = True
            user.is_verified = True
            user.verification_code          = ''
            user.verification_code_expires  = None
            user.save()

            # Clean up session
            del request.session['pending_verification_email']

            # Log user in immediately
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('landing_page')

    return render(request, 'users/verify_email.html', {
        'form':  form,
        'email': email,
    })


# ================================================================
# RESEND VERIFICATION EMAIL
# ================================================================
@require_POST
def resend_verification_view(request):
    """
    POST only — resends the 6-digit code to the pending email.
    Rate-limited to 1 resend per 60 seconds via session timestamp.
    """
    email = (
        request.POST.get('email')
        or request.session.get('pending_verification_email')
    )

    if not email:
        messages.error(request, 'Brak adresu e-mail. Zarejestruj się ponownie.')
        return redirect('users:register')

    # ── Rate limit: max 1 resend per 60 seconds ──
    last_resend = request.session.get('last_resend_ts')
    if last_resend:
        elapsed = (timezone.now() - datetime.fromisoformat(last_resend)).seconds
        if elapsed < 60:
            remaining = 60 - elapsed
            messages.warning(
                request,
                f'Poczekaj jeszcze {remaining}s przed ponownym wysłaniem.'
            )
            return redirect('users:verify_email')

    try:
        user = User.objects.get(email=email, is_active=False)
    except User.DoesNotExist:
        # Either already verified or doesn't exist — don't leak info
        messages.info(
            request,
            'Jeśli konto istnieje i nie jest zweryfikowane, '
            'wysłaliśmy nowy kod.'
        )
        return redirect('users:verify_email')

    send_verification_email(user)

    # Save timestamp for rate limiting
    request.session['pending_verification_email'] = email
    request.session['last_resend_ts'] = timezone.now().isoformat()

    messages.success(request, f'Nowy kod wysłany na {email}.')
    return redirect('users:verify_email')


# ================================================================
# DASHBOARD (placeholder — replace with real view)
# ================================================================
# @login_required
# def dashboard_view(request):
#     return render(request, 'users/dashboard.html', {
#         'user': request.user,
#     })
