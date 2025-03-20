from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static

app_name = 'adm'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('empresa.urls'), name='adm'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
