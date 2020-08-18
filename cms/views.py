from django.shortcuts import render
from django.http import HttpResponse

from .models import WhereFindHelp

def test(request):
    articles = WhereFindHelp.objects.all()
    return render(request, template_name='org.html', context={'articles':articles})

# Create your views here.
