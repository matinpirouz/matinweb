from django.shortcuts import render
from .models import Page, Province

def home(request):
    pages = Page.objects.all()
    return render(request, 'index.html', {'pages': pages})

def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def coming_soon(request):
    return render(request, 'errors/soon.html')

def prayer(request):
    provinces = Province.objects.all()
    return render(request, 'pages/prayer.html', {'provinces': provinces})