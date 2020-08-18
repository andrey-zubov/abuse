from django.shortcuts import render
from django.http import HttpResponse

from .models import WhereFindHelp, Page, Block

def test(request):
    articles = WhereFindHelp.objects.all()
    return render(request, template_name='org.html', context={'articles':articles})


def wtf(request):
    pages = Page.objects.all()
    blocks = Block.objects.all()
    return render(request, template_name='wtf_temp.html', context={'test': pages,
                                                                   'blocks': blocks})
