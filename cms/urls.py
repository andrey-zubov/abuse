from django.urls import path, include
from .views import main_page, articles_by_cat

urlpatterns = [
    path('abuse/', main_page),
    path('abuse/<slug>', articles_by_cat, name='slug_url'),
]