from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('app_chat.urls')),
    path('users/', include('app_users.urls')),
]

urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


