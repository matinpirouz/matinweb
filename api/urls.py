from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register_view),
    path('cities/<int:province_code>/', cities_by_province),
]
