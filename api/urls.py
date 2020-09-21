from django.urls import path, include

from .views import (
    OrgAPIView,
    RegionAPI,
    AreaAPI,
    CityAPI
)

urlpatterns = [
    path('orgs/', OrgAPIView.as_view()),
    path('regions/', RegionAPI.as_view()),
    path('areas/', AreaAPI.as_view()),
    path('cities/', CityAPI.as_view()),

    ]