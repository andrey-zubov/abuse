from django.urls import path, include
from .views import test, wtf

urlpatterns = [
    path('org/', test),

    path('wtf/', wtf)
]