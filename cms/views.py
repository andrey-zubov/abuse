from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from .forms import OrgForm, VacancyForm, EventForm
from .utils import check_city

from .models import (
    Page,
    NewsPage,
    Organizations,
    City,
    ServicesType,
    OrganizationServices,
    Question,
    Choice,
    Answer,
    HelpFile,
    FAQ,
    OrgTemplate,
    Feedback,
    BackCall
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
    all_quiz = Question.objects.filter(is_active=True)
    org_settings = OrgTemplate.objects.latest('id')
    down_cats = Page.objects.filter(test_category='down')
    up_cats = Page.objects.filter(test_category='up')

    return render(
        request,
        template_name='organizations.html',
        context={
            'org': org,
            'quiz': all_quiz,
            'org_settings': org_settings,
            'up_cats' : up_cats,
            'down_cats' : down_cats,
        }
    )


def news_view(request):
    news = NewsPage.objects.filter(template_key='widgets/news_widget.html')
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
    down_cats = Page.objects.filter(test_category='down')
    up_cats = Page.objects.filter(test_category='up')

    return render(
        request,
        template_name='add_new_org.html',
        context={
            'form': form,
            'vac_form': vac_form,
            'event_form': event_form,
            'all_types': all_types,
            'down_cats': down_cats,
            'up_cats': up_cats,

        }
    )


def create_org(request):  # ajax

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
        print(form.errors)


def create_vac(request):  # ajax
    vac_form = VacancyForm(request.GET)
    if vac_form.is_valid():
        new_vac = vac_form.save(commit=False)
        new_vac.city = check_city(request.GET['pre_city'])
        new_vac.save()
        return HttpResponse('save')
    else:
        print(vac_form.errors)


def create_event(request):  # ajax
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


def create_feedback(request):  # ajax
    print(request.GET)
    if request.GET.__contains__('message_text'):
        print('msg')
        Feedback.objects.create(
            text=request.GET['message_text']
        )
    elif request.GET.__contains__('cal_tel'):
        BackCall.objects.create(
            name=request.GET['cal_name'],
            tel=request.GET['cal_tel']
        )
    return HttpResponse(1)


def testnews(request, slug):
    feincms_page = NewsPage.objects.get(slug=slug)
    down_cats = Page.objects.filter(test_category='down')
    up_cats = Page.objects.filter(test_category='up')

    return render(
        request,
        template_name='widgets/newspage.html',
        context={
            'feincms_page': feincms_page,
            'up_cats': up_cats,
            'down_cats': down_cats,
        }
    )

