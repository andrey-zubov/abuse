from django.shortcuts import render
from django.http import HttpResponse

from .models import Articles, Page, Block, Main_Cat, Organizations, City, ServicesType


def main_page(request):
    all_cats = Main_Cat.objects.filter(is_active=True)
    down_cats = all_cats.filter(header_menu='down')
    up_cats = all_cats.filter(header_menu='up')
    return render(
        request,
        template_name='main_page.html',
        context={'down_cats': down_cats,
                 'up_cats': up_cats,
                 })


def articles_by_cat(request, slug):
    category_number = Main_Cat.objects.get(slug=slug).id
    orgs = Organizations.objects.all()
    all_cites = City.objects.all()
    all_types = ServicesType.objects.all()

    articles = Articles.objects.filter(category__id=category_number)
    return render(
        request,
        template_name='Main_Article.html',
        context={'articles': articles,
                 'orgs': orgs,
                 'all_cites': all_cites,
                 'all_types': all_types,
                 })

