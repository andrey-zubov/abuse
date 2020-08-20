from django.shortcuts import render
from django.http import HttpResponse

from .models import Articles, Page, Block, Main_Cat


def main_page(request):
    cats = Main_Cat.objects.all()
    return render(request, template_name='main_page.html', context={'cats':cats})


def articles_by_cat(request, slug):
    category_number = Main_Cat.objects.get(slug=slug).id

    articles = Articles.objects.filter(category__id=category_number)
    return render(request, template_name='org.html', context={'articles':articles})

