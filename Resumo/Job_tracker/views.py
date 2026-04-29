from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_name = 'job_tracker'

@login_required
def index(request):
    return render(request, 'job_tracker/index.html')