
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('', include('Authentication.urls')),
    path('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('post/', include('FknAp.urls')),
    path('tags/', include('tags.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)
    


