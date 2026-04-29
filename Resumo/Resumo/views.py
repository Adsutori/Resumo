from django.shortcuts import render

def landing_page(request):
    return render(request, 'index.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')