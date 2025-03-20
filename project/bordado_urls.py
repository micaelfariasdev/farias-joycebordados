from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

app_name = 'bordado'


urlpatterns = [
    path('', include('joycebordados.urls'), ),  # Para o subdomínio bordado
    path('cliente/', include('clientes.urls'), ),  # Para o subdomínio bordado
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
