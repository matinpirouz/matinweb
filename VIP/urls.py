from django.urls import path
from .views import *

app_name = 'VIP'

urlpatterns = [
    path('create_invoice', create_invoice, name='create_invoice'),
]