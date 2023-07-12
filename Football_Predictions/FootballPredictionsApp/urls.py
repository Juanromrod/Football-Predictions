from django.urls import path
from .views import calcular_probabilidad

urlpatterns = [
    path('', calcular_probabilidad, name='calcular_probabilidad'),
]