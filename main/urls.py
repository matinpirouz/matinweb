from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('soon/', coming_soon, name='coming_soon'),
    path('prayer/', prayer, name='prayer'),
]