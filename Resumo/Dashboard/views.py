import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import CV
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F




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
# WIDOK — Dashboard (lista CV)
# ──────────────────────────────────────────────

@login_required
def dashboard(request):
    cvs = CV.objects.filter(user=request.user).order_by('-updated_at')
    context = {
        'cvs':       cvs,
        'cvs_count': cvs.count(),
    }
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

    return render(request, 'dashboard/cv-new.html')


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
    context = {
        'cv':          cv,
        'cv_content':  json_module.dumps(cv.content if cv.content else {}),
    }
    return render(request, 'dashboard/cv-editor.html', context)


@login_required
def download_pdf(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id, user=request.user)
    CV.objects.filter(id=cv_id).update(download_count=F('download_count') + 1)

    template_map = {
        'classic': 'dashboard/pdf/cv-classic.html',
        'modern':  'dashboard/pdf/cv-modern.html',
        'minimal': 'dashboard/pdf/cv-minimal.html',
    }
    template_name = template_map.get(cv.template, 'dashboard/pdf/cv-classic.html')

    html_string = render_to_string(template_name, {
        'cv':      cv,
        'content': cv.content or {},
    }, request=request)

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    safe_title = cv.title.replace(' ', '_').replace('/', '-')[:50]
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{safe_title}.pdf"'
    return response