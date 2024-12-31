from django.contrib import admin
from django.urls import path, include
from .local_setting import ADMIN_PATH
from django.conf import settings
from django.conf.urls.static import static
from users.views import index

urlpatterns = [
    path(ADMIN_PATH, admin.site.urls),
    path('', index, name='landing_page'),
    path('users/', include('users.urls')),
    path('menu/', include('menu.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
