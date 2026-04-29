from django.shortcuts import render

def landing_page(request):
    return render(request, 'index.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def error_404(request, exception=None):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

def test_404(request):
    return render(request, '404.html', status=404)

def test_500(request):
    return render(request, '500.html', status=500)