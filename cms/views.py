from django.shortcuts import render
from django.http import HttpResponse

from .models import WhereFindHelp, Page, Block


def main_page(request):
    return render(request, template_name='main_page.html')


def find_help(request):
    articles = WhereFindHelp.objects.filter(is_active=True)
    return render(request, template_name='org.html', context={'articles':articles})


def co_dependent(request):
    return HttpResponse('codep')


def wtf(request):
    pages = Page.objects.filter(id=2)
    blocks = Block.objects.all()
    return render(request, template_name='wtf_temp.html', context={'test': pages,
                                                                   'blocks': blocks})
