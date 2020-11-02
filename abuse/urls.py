from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import cms

urlpatterns = [
    path('admin-abuse/', admin.site.urls),
    path('', include('cms.urls')),
    path('api/', include('api.urls')),
    path('admin/', cms.views.admin_choice),
]

urlpatterns += [
    path(r'', include('feincms.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
