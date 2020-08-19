from django.urls import path, include
from .views import test, wtf, main_page

urlpatterns = [
    path('', main_page),
    path('org/', test),

    path('wtf/', wtf)
]