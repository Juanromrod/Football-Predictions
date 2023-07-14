from django.urls import path
from .views import calcular_probabilidad
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', calcular_probabilidad, name='calcular_probabilidad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)