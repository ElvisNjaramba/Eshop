from django.contrib import admin
from django.urls import path  , include
from django.conf.urls.static import static
from . import settings
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('store.urls')),   
    path('inventory/', include('base.urls')),
    path('invoice', include('invoice.urls')),
    path('inventory/login' , include('invoice.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
