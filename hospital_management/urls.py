from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from management.views import signin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include('management.urls')),
    path('sign-in/', signin, name='signin'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
