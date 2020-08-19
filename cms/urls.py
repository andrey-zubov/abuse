from django.urls import path, include
from .views import find_help, wtf, main_page

urlpatterns = [
    path('', main_page),
    path('org/', find_help),

    path('wtf/', wtf)
]