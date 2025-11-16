from django.shortcuts import render
from .models import page

def home(request):
    pages = page.objects.all()
    return render(request, 'index.html', {'pages': pages})