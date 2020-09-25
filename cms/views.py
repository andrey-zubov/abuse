from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from .forms import OrgForm, VacancyForm, EventForm
from django.forms import inlineformset_factory
import re

from .models import (
    Page,
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
    down_cats = Page.objects.filter(test_category='down')
    up_cats = Page.objects.filter(test_category='up')

    return render(
        request,
        template_name='main_page.html',
        context={'down_cats': down_cats,
                 'up_cats': up_cats,
                 })


def help_file(request):
    file = HelpFile.objects.latest('id')
    return FileResponse(open(file.get_file, 'rb'))


def get_answer(request):  # handle quiz answer
    if request.GET.__contains__('answer_for'):  # hold an answer in db
        question = Question.objects.get(title=request.GET['answer_for'])
        choice = Choice.objects.get(
            Q(question=question) & Q(title=request.GET[question.title])
        )
        save_answer = Answer.objects.create(
            question_id=question.id,
            choice=choice
        )
    return HttpResponse(111)

# def megapage(request, slug):
#     this_category = Main_Cat.objects.get(slug=slug)
#
#     if request.GET.__contains__('answer_for'):  # hold an answer in db
#         question = Question.objects.get(title=request.GET['answer_for'])
#         choice = Choice.objects.get(
#             Q(question=question) & Q(title=request.GET[question.title])
#         )
#         save_answer = Answer.objects.create(
#             question_id=question.id,
#             choice=choice
#         )
#
#     if this_category.org_widget:
#         orgs = Organizations.objects.all().prefetch_related('organizationservices_set')
#         org_widget_flag = True
#     else:
#         orgs = None
#         org_widget_flag = False
#
#     all_cites = City.objects.filter()
#     all_types = ServicesType.objects.filter()
#     pages = Page.objects.filter(
#         Q(template_key='widgets/single_article.html') & Q(category__id=this_category.id)
#     )
#     questions = Question.objects.all().prefetch_related('choice_set')
#
#     show_help = this_category.help_widget
#     return render(
#         request,
#         template_name='widgets/articles_by_cat_mk2.html',
#         context={
#             'pages': pages,
#             'questions': questions,
#             'orgs': orgs,
#             'all_cites': all_cites,
#             'all_types': all_types,
#             'show_help': show_help,
#             'org_widget_flag': org_widget_flag,
#             'this_category': this_category,
#     })


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
    news = Page.objects.filter(template_key='widgets/news_widget.html')
    down_cats = Page.objects.filter(test_category='down')
    up_cats = Page.objects.filter(test_category='up')

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
    all_types = ServicesType.objects.filter()
    form = OrgForm()
    vac_form = VacancyForm()
    event_form = EventForm()


    return render(
        request,
        template_name='add_new_org.html',
        context={
            'form': form,
            'vac_form': vac_form,
            'event_form': event_form,
            'all_types': all_types

        }
    )


def create_org(request):
    org_type = ServicesType.objects.get(
        id=request.GET['org_type']
    )
    city = check_city(request.GET['pre_city'])
    form = OrgForm(request.GET)
    if form.is_valid():
        new_org = form.save(commit=False)
        new_org.city = city
        new_org.slug = request.GET['title']
        new_org.save()
        new_org.get_services.create(
            org_type_id=request.GET['org_type'],
            organization_id=new_org.id,
            conf='0',
            stuff='0',
            payment='0'
        )
        new_org.save()

        return HttpResponse('save')
    else:
        return HttpResponse('fail')



def create_vac(request):
    vac_form = VacancyForm(request.GET)
    if vac_form.is_valid():
        new_vac = vac_form.save(commit=False)
        new_vac.city = check_city(request.GET['pre_city'])
        new_vac.save()
        return HttpResponse('save')

    else:
        print(vac_form.errors)
        return HttpResponse('fail')


def create_event(request):
    event_form = EventForm(request.GET)
    if event_form.is_valid():
        new_event = event_form.save(commit=False)
        if request.POST.__contains__('free_entrance'):
            new_event.payment = 0
        new_event.city = check_city(request.GET['pre_city'])
        new_event.save()
        return HttpResponse('save')
    else:
        print(event_form.errors)
        return HttpResponse('fail')





def check_city(looknig_city):  # TODO move to utils
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




