from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from .forms import OrgForm
from django.forms import inlineformset_factory

from .models import (
    Page,
    Main_Cat,
    Organizations,
    City,
    ServicesType,
    OrganizationServices,
    Question,
    Choice,
    Answer,
    HelpFile,
    FAQ
)


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


def help_file(request):
    file = HelpFile.objects.latest('id')
    return FileResponse(open(file.get_file, 'rb'))


def megapage(request, slug):
    this_category = Main_Cat.objects.get(slug=slug)

    if request.GET.__contains__('answer_for'):  # hold an answer in db
        question = Question.objects.get(title=request.GET['answer_for'])
        choice = Choice.objects.get(
            Q(question=question) & Q(title=request.GET[question.title])
        )
        save_answer = Answer.objects.create(
            question_id=question.id,
            choice=choice
        )

    if this_category.org_widget:
        orgs = Organizations.objects.all().prefetch_related('organizationservices_set')
        org_widget_flag = True
    else:
        orgs = None
        org_widget_flag = False

    employment_flag = True if this_category.employment_widget else False

    all_cites = City.objects.filter()
    all_types = ServicesType.objects.filter()
    pages = Page.objects.filter(
        Q(template_key='widgets/single_article.html') & Q(category__id=this_category.id)
    )
    questions = Question.objects.all().prefetch_related('choice_set')

    show_help = this_category.help_widget
    # show_hiv = this_category.help_widget
    # show_relapse = this_category.relapse_widget
    return render(
        request,
        template_name='widgets/articles_by_cat.html',
        context={
            'pages': pages,
            'questions': questions,
            'orgs': orgs,
            'all_cites': all_cites,
            'all_types': all_types,
            'show_help': show_help,
            'org_widget_flag': org_widget_flag,
            'this_category': this_category,
            'employment_flag': employment_flag
    })


def faq(request):
    faq = FAQ.objects.all()
    questions = Question.objects.all().prefetch_related('choice_set')
    return render(
        request,
        template_name='faq.html',
        context={'faq': faq,
                 'questions': questions}
    )


def org_info(request, slug):
    org = Organizations.objects.get(slug=slug)

    return render(
        request,
        template_name='organizations.html',
        context={'org': org}
    )


def news_view(request):
    news = Page.objects.filter(template_key='widgets/base_widget.html')
    all_cats = Main_Cat.objects.filter(is_active=True)
    down_cats = all_cats.filter(header_menu='down')
    up_cats = all_cats.filter(header_menu='up')

    return render(
        request,
        template_name='news.html',
        context={
            'news': news,
            'down_cats': down_cats,
            'up_cats': up_cats,
        }
    )


def add_new_org(request):
    if request.method == 'POST':
        #print(request.POST)
        org_type = ServicesType.objects.get(
            id=request.POST['org_type']
        )
        city = check_city(request.POST['pre_city'])
        form = OrgForm(request.POST)

        if form.is_valid():
            new_org = form.save(commit=False)
            new_org.city = city
            new_org.slug = request.POST['title']
            new_org.save()
            return HttpResponse('save')

        else:
            print(form.errors)
        return HttpResponse('post')
    else:
        all_types = ServicesType.objects.filter()
        form = OrgForm()


        return render(
            request,
            template_name='add_new_org.html',
            context={
                'form': form,
                'all_types': all_types

            }
        )

import re
def check_city(looknig_city):
    pre_city = re.sub(r'\w+\.', '', looknig_city).strip().capitalize()  # clear data from г.
    all_cityes = City.objects.all()
    if all_cityes.filter(title__iexact=pre_city).exists():
        return all_cityes.get(title__iexact=pre_city)
    elif all_cityes.filter(title__icontains=pre_city).exists():
        return all_cityes.get(title__icontains=pre_city)
    else:
        new_city = City.objects.create(
            title=pre_city
        )
        return new_city
