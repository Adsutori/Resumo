import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from .models import CV
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
import hashlib
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from .models import CV, CVView



# ──────────────────────────────────────────────
# HELPER — obliczanie postępu wypełnienia CV
# ──────────────────────────────────────────────

def calculate_progress(content: dict) -> int:
    """
    Oblicza % wypełnienia CV na podstawie zawartości content.

    Wagi sekcji:
      personal   → max 20% (6 pól, każde ~3.33%)
      summary    → 15%
      experience → 20% jeśli min. 1 wpis
      education  → 15% jeśli min. 1 wpis
      skills     → 10% jeśli min. 3 umiejętności
      languages  → 10% jeśli min. 1 język
      links      → 10% jeśli min. 1 link
    """
    score = 0

    # ── Dane osobowe (max 20%) ──
    personal       = content.get('personal', {})
    personal_fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'position']
    filled_personal = sum(1 for f in personal_fields if personal.get(f, '').strip())
    score += round((filled_personal / len(personal_fields)) * 20)

    # ── Podsumowanie (15%) ──
    summary = content.get('summary', '')
    if isinstance(summary, str) and len(summary.strip()) > 20:
        score += 15

    # ── Doświadczenie (20%) ──
    experience = content.get('experience', [])
    if isinstance(experience, list) and len(experience) >= 1:
        # Sprawdź czy przynajmniej jeden wpis ma wypełnione kluczowe pola
        for exp in experience:
            if exp.get('company', '').strip() and exp.get('position', '').strip():
                score += 20
                break

    # ── Wykształcenie (15%) ──
    education = content.get('education', [])
    if isinstance(education, list) and len(education) >= 1:
        for edu in education:
            if edu.get('school', '').strip():
                score += 15
                break

    # ── Umiejętności (10%) ──
    skills = content.get('skills', [])
    if isinstance(skills, list):
        filled_skills = [s for s in skills if isinstance(s, str) and s.strip()]
        if len(filled_skills) >= 3:
            score += 10

    # ── Języki (10%) ──
    languages = content.get('languages', [])
    if isinstance(languages, list) and len(languages) >= 1:
        for lang in languages:
            if lang.get('name', '').strip():
                score += 10
                break

    # ── Linki (10%) ──
    links = content.get('links', {})
    if isinstance(links, dict):
        filled_links = [v for v in links.values() if isinstance(v, str) and v.strip()]
        if len(filled_links) >= 1:
            score += 10

    return min(score, 100)


# ──────────────────────────────────────────────
# HELPER — ukończenie profilu (0–100%)
# ──────────────────────────────────────────────

def _calculate_profile_completion(user, cvs):
    """
    Liczy % ukończenia profilu na podstawie:
      - danych konta użytkownika (40%)
      - najlepiej wypełnionego CV (60%)
    """
    score = 0

    # ── Dane konta (max 40%) ──
    account_fields = {
        'first_name': 10,
        'last_name':  10,
        'email':      10,
        'avatar':     10,
    }
    for field, weight in account_fields.items():
        val = getattr(user, field, None)
        if val:
            score += weight

    # ── Najlepiej wypełnione CV (max 60%) ──
    if cvs:
        best_cv_progress = max(cv.progress for cv in cvs)
        score += round(best_cv_progress * 0.60)

    return min(score, 100)


# ──────────────────────────────────────────────
# HELPER — dni aktywności
# ──────────────────────────────────────────────

def _calculate_activity_days(user):
    """
    Liczy dni aktywności jako:
    - Ile unikalnych dni w ostatnich 30 dniach
      user miał wyświetlenia swoich CV (proxy aktywności).
    - Minimum 1 jeśli user jest zalogowany dziś.
    """
    from django.utils import timezone
    from datetime import timedelta
    from .models import CVView
    from django.db.models.functions import TruncDate

    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Unikalne dni z wyświetleń CV usera w ostatnich 30 dniach
    unique_days = (
        CVView.objects
        .filter(
            cv__user=user,
            viewed_at__gte=thirty_days_ago,
        )
        .annotate(day=TruncDate('viewed_at'))
        .values('day')
        .distinct()
        .count()
    )

    # Zawsze liczymy dzień rejestracji i dzień ostatniego logowania
    base_days = set()
    if user.created_at:
        base_days.add(user.created_at.date())
    if user.last_login:
        base_days.add(user.last_login.date())

    # Dzisiaj też liczymy (user jest teraz zalogowany)
    base_days.add(timezone.now().date())

    return max(unique_days, len(base_days))


# ──────────────────────────────────────────────
# WIDOK — Dashboard (lista CV)
# ──────────────────────────────────────────────

@login_required
def dashboard(request):
    from django.utils import timezone
    from datetime import timedelta

    cvs = CV.objects.filter(user=request.user).order_by('-updated_at')

    # ── Licznik pobrań PDF (suma wszystkich CV usera) ──
    total_downloads = sum(cv.download_count for cv in cvs)

    # ── Licznik wyświetleń (suma wszystkich CV usera) ──
    total_views = sum(cv.view_count for cv in cvs)

    # ── Ukończenie profilu ──
    profile_completion = _calculate_profile_completion(request.user, cvs)

    # ── Dni aktywności (ostatnie 30 dni z last_login) ──
    activity_days = _calculate_activity_days(request.user)

    context = {
        'cvs':                cvs,
        'cvs_count':          cvs.count(),
        'total_downloads':    total_downloads,
        'total_views':        total_views,
        'profile_completion': profile_completion,
        'activity_days':      activity_days,
    }

    if profile_completion == 100:
            from Notifications.utils import notify_profile_complete
            from Notifications.models import Notification
            if not Notification.objects.filter(
                user=request.user, type='profile'
            ).exists():
                notify_profile_complete(request.user)

    return render(request, 'dashboard/dashboard.html', context)


# ──────────────────────────────────────────────
# WIDOK — Tworzenie nowego CV
# ──────────────────────────────────────────────

@login_required
def create_cv(request):
    """
    GET  → strona wyboru szablonu
    POST → tworzy CV i przekierowuje do edytora
    """
    
    if request.method == 'POST':
        title    = request.POST.get('title', '').strip()
        template = request.POST.get('template', 'classic')

        if template not in ['classic', 'modern', 'minimal']:
            template = 'classic'

        if not title:
            base  = 'Moje CV'
            count = CV.objects.filter(user=request.user, title__startswith=base).count()
            title = base if count == 0 else f'{base} {count + 1}'

        cv = CV.objects.create(
            user     = request.user,
            title    = title,
            template = template,
        )
        return redirect('dashboard:edit_cv', cv_id=cv.id)

    # GET — opcjonalny pre-selected template z query param
    preselected = request.GET.get('template', 'classic')
    if preselected not in ['classic', 'modern', 'minimal']:
        preselected = 'classic'

    return render(request, 'dashboard/cv-new.html', {'preselected_template': preselected})



# ──────────────────────────────────────────────
# WIDOK — Edytor CV
# ──────────────────────────────────────────────

@login_required
def edit_cv(request, cv_id):
    """
    GET  → renderuje edytor z danymi CV
    POST (JSON) → zapisuje content + title, zwraca JsonResponse
    """
    # Pobierz CV — tylko właściciela, inaczej 404
    cv = get_object_or_404(CV, id=cv_id, user=request.user)

    # ── Obsługa autosave (POST JSON) ──
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Nieprawidłowy JSON'}, status=400)

            # Zaktualizuj tytuł jeśli przesłany
            new_title = body.get('title', '').strip()
            if new_title:
                cv.title = new_title

            # Zaktualizuj content
            new_content = body.get('content', {})
            if isinstance(new_content, dict):
                cv.content = new_content

            # Zaktualizuj design
            new_design = body.get('design', {})
            if isinstance(new_design, dict) and new_design:
                cv.design = new_design

            # Oblicz postęp
            cv.progress = calculate_progress(cv.content)
            cv.save()

            return JsonResponse({
                'status':   'ok',
                'progress': cv.progress,
                'title':    cv.title,
            })

        return JsonResponse({'status': 'error', 'message': 'Wymagany Content-Type: application/json'}, status=415)

    # ── GET — renderuj edytor ──
    import json as json_module
    from .models import DEFAULT_DESIGN

    # Scal domyślny design z zapisanym w bazie
    design = {**DEFAULT_DESIGN, **(cv.design or {})}

    context = {
        'cv':         cv,
        'cv_content': json_module.dumps(cv.content if cv.content else {}),
        'cv_design':  json_module.dumps(design),
    }
    return render(request, 'dashboard/cv-editor.html', context)


def darken_hex(hex_color: str, factor: float) -> str:
    """Przyciemnia kolor hex. factor: 0.0=czarny, 1.0=oryginalny."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c*2 for c in hex_color)
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        return '#1a1a2e'
    r = round(r * factor)
    g = round(g * factor)
    b = round(b * factor)
    return f'#{r:02x}{g:02x}{b:02x}'


@login_required
def download_pdf(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, user=request.user)

    from .models import DEFAULT_DESIGN
    merged_design = {**DEFAULT_DESIGN, **(cv.design or {})}
    cv.design = merged_design

    accent = merged_design.get('accent_color', '#6C63FF')

    # Wylicz ciemne odcienie — tak samo jak JS w edytorze
    dark_base = darken_hex(accent, 0.18)   # gradient nagłówka — lewa strona
    dark_mid  = darken_hex(accent, 0.25)   # sidebar góra
    dark_deep = darken_hex(accent, 0.15)   # sidebar dół

    template_map = {
        'classic': 'dashboard/pdf/cv-classic.html',
        'modern':  'dashboard/pdf/cv-modern.html',
        'minimal': 'dashboard/pdf/cv-minimal.html',
    }
    template_name = template_map.get(cv.template, 'dashboard/pdf/cv-classic.html')

    html = render_to_string(template_name, {
        'cv':        cv,
        'content':   cv.content or {},
        'dark_base': dark_base,
        'dark_mid':  dark_mid,
        'dark_deep': dark_deep,
    }, request=request)

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    CV.objects.filter(pk=cv_id).update(download_count=F('download_count') + 1)

    safe_title = cv.title.replace(' ', '_').replace('/', '-')[:50]
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{safe_title}.pdf"'
    return response


# ──────────────────────────────────────────────
# WIDOK — Duplikowanie CV
# ──────────────────────────────────────────────

@login_required
@require_POST
def duplicate_cv(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id, user=request.user)

    cv.pk           = None          # Django utworzy nowy obiekt
    cv.title        = f'Kopia — {cv.title}'
    cv.share_token  = uuid.uuid4()  # nowy unikalny token
    cv.is_shared    = False
    cv.download_count = 0
    cv.view_count   = 0
    cv.save()

    messages.success(request, f'CV zostało zduplikowane jako „{cv.title}".')
    return redirect('dashboard:dashboard')


# ──────────────────────────────────────────────
# WIDOK — Usuwanie CV
# ──────────────────────────────────────────────

@login_required
@require_POST
def delete_cv(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id, user=request.user)
    title = cv.title
    cv.delete()

    messages.success(request, f'CV „{title}" zostało usunięte.')
    return redirect('dashboard:dashboard')


# ── Strona główna sekcji ──────────────────────────────────
@login_required
def share_dashboard(request):
    cvs = CV.objects.filter(user=request.user).order_by('-updated_at')

    week_ago = timezone.now() - timedelta(days=7)

    total_views  = 0
    active_count = 0
    week_views   = 0

    for cv in cvs:
        cv.views_week = cv.views.filter(viewed_at__gte=week_ago).count()
        cv.share_url   = cv.get_share_url(request)
        total_views  += cv.view_count
        week_views   += cv.views_week
        if cv.is_share_active():
            active_count += 1

    return render(request, 'dashboard/share-dashboard.html', {
        'cvs':          cvs,
        'total_views':  total_views,
        'active_count': active_count,
        'week_views':   week_views,
    })


# ── Toggle udostępniania ──────────────────────────────────
@login_required
@require_POST
def toggle_share(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, user=request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    cv.is_shared = data.get('is_shared', False)

    expires = data.get('expires')
    if expires:
        try:
            from django.utils.dateparse import parse_datetime
            parsed = parse_datetime(expires)
            if parsed:
                # Jeśli brak tzinfo — dodaj lokalną strefę
                if parsed.tzinfo is None:
                    from django.utils import timezone as tz
                    parsed = tz.make_aware(parsed)
                cv.share_expires = parsed
            else:
                cv.share_expires = None
        except Exception:
            cv.share_expires = None
    else:
        cv.share_expires = None

    cv.save(update_fields=['is_shared', 'share_expires'])

    return JsonResponse({
        'status':    'ok',
        'is_shared': cv.is_shared,
        'share_url': cv.get_share_url(request),
        'is_active': cv.is_share_active(),
    })


# ── Regeneracja tokenu ────────────────────────────────────
@login_required
@require_POST
def regenerate_token(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, user=request.user)
    cv.share_token = uuid.uuid4()
    cv.save(update_fields=['share_token'])

    return JsonResponse({
        'status':    'ok',
        'share_url': cv.get_share_url(request),
    })


# ── Statystyki wyświetleń (JSON) ──────────────────────────
@login_required
def share_stats(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, user=request.user)

    # Ostatnie 7 dni
    week_ago = timezone.now() - timedelta(days=7)
    daily = (
        cv.views
        .filter(viewed_at__gte=week_ago)
        .annotate(day=TruncDate('viewed_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Wypełnij brakujące dni zerami
    days_map = {entry['day'].isoformat(): entry['count'] for entry in daily}
    labels, values = [], []
    for i in range(6, -1, -1):
        day = (timezone.now() - timedelta(days=i)).date()
        labels.append(day.strftime('%d.%m'))
        values.append(days_map.get(day.isoformat(), 0))

    return JsonResponse({
        'total':      cv.view_count,
        'week_total': sum(values),
        'labels':     labels,
        'values':     values,
    })


# ── Publiczny widok CV (już masz, tylko dodaj CVView) ─────
def share_cv(request, token):
    cv = get_object_or_404(CV, share_token=token)

    if not cv.is_share_active():
        raise Http404("Ten link wygasł lub CV nie jest udostępnione.")

    # Zapisz wyświetlenie z zahashowanym IP
    ip = request.META.get('REMOTE_ADDR', '')
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:32]
    CVView.objects.create(cv=cv, ip_hash=ip_hash)
    CV.objects.filter(pk=cv.pk).update(view_count=F('view_count') + 1)
    cv.refresh_from_db()

    from .models import DEFAULT_DESIGN
    merged_design = {**DEFAULT_DESIGN, **(cv.design or {})}
    cv.design = merged_design

    accent    = merged_design.get('accent_color', '#6C63FF')
    dark_base = darken_hex(accent, 0.18)
    dark_mid  = darken_hex(accent, 0.25)
    dark_deep = darken_hex(accent, 0.15)

    template_map = {
        'classic': 'dashboard/pdf/cv-classic.html',
        'modern':  'dashboard/pdf/cv-modern.html',
        'minimal': 'dashboard/pdf/cv-minimal.html',
    }
    template_name = template_map.get(cv.template, 'dashboard/pdf/cv-classic.html')

    cv_html = render_to_string(template_name, {
        'cv':        cv,
        'content':   cv.content or {},
        'is_public': True,
        'dark_base': dark_base,
        'dark_mid':  dark_mid,
        'dark_deep': dark_deep,
    }, request=request)

    return render(request, 'dashboard/cv-share.html', {
        'cv':      cv,
        'cv_html': cv_html,
    })