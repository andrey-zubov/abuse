from django.shortcuts import render
from django.http import HttpResponse

from .models import where_find_help

def test(request):
    widgets = where_find_help.objects.all()
    return render(request, template_name='org.html', context={'widgets':widgets})

# Create your views here.
