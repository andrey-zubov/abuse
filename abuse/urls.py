from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import cms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('abuse/', include('cms.urls')),
    path('api/', include('api.urls')),
    path('chooser/', cms.views.admin_choice),
]

urlpatterns += [
    path(r'abuse/', include('feincms.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
