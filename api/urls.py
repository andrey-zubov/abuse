from django.urls import path, include

from .views import OrgAPIView

urlpatterns = [
    path('orgs/', OrgAPIView.as_view()),
    ]