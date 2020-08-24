from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

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


def articles_by_cat(request, slug, choosed_city=None, choosed_type=None):
    if not request.GET.__contains__('is_org_finder'):
        orgs = Organizations.objects.all()
    else:
        city_id = int(request.GET['choosed_city'])
        type_id = int(request.GET['choosed_type'])
        orgs = Organizations.objects.filter(
            Q(city__id=city_id) & Q(organizationservices__org_type=type_id)
        )


    category_number = Main_Cat.objects.get(slug=slug).id
    all_cites = City.objects.filter()
    all_types = ServicesType.objects.filter()
    all_cats = Main_Cat.objects.filter(is_active=True)
    down_cats = all_cats.filter(header_menu='down')
    up_cats = all_cats.filter(header_menu='up')

    articles = Articles.objects.filter(category__id=category_number)
    return render(
        request,
        template_name='Main_Article.html',
        context={'articles': articles,
                 'orgs': orgs,
                 'all_cites': all_cites,
                 'all_types': all_types,
                 'all_cats': all_cats,
                 'down_cats': down_cats,
                 'up_cats': up_cats,
                 })


def org_info(request, slug):
    org = Organizations.objects.get(slug=slug)

    return render(
        request,
        template_name='organizations.html',
        context={'org': org}
    )


def news_view(request):
    return HttpResponse(444)