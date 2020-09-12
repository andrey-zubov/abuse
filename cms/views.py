from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from .forms import OrgForm
from django.forms import inlineformset_factory

from .models import (
    Articles,
    Page,
    Main_Cat,
    Organizations,
    City,
    ServicesType,
    OrganizationServices,
    Question,
    Choice,
    Answer,
    HelpFile
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

    all_cites = City.objects.filter()
    all_types = ServicesType.objects.filter()
    pages = Page.objects.filter(
        Q(template_key='widgets/single_article.html') & Q(category__id=this_category.id)
    )
    questions = Question.objects.all().prefetch_related('choice_set')

    show_help = this_category.help_widget
    show_hiv = this_category.help_widget
    show_relapse = this_category.relapse_widget
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
            'show_hiv': show_hiv,
            'show_relapse': show_relapse,
            'org_widget_flag': org_widget_flag,
            'this_category': this_category
    })

#
# def articles_by_cat(request, slug, choosed_city=None, choosed_type=None):
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
#     this_category = Main_Cat.objects.get(slug=slug)
#
#     show_help = this_category.help_widget
#     show_hiv = this_category.help_widget
#     show_relapse = this_category.relapse_widget
#
#     if this_category.org_widget:
#         orgs = Organizations.objects.all().prefetch_related('organizationservices_set')
#         org_widget_flag = True
#     else:
#         orgs = None
#         org_widget_flag = False
#
#     category_number = Main_Cat.objects.get(slug=slug).id
#     all_cites = City.objects.filter()
#     all_types = ServicesType.objects.filter()
#     all_cats = Main_Cat.objects.filter(is_active=True)
#     down_cats = all_cats.filter(header_menu='down')
#     up_cats = all_cats.filter(header_menu='up')
#     questions = Question.objects.all().prefetch_related('choice_set')
#     articles = Articles.objects.filter(category__id=category_number)
#     return render(
#         request,
#         template_name='Main_Article.html',
#         context={'articles': articles,
#                  'orgs': orgs,
#                  'org_widget_flag': org_widget_flag,
#                  'all_cites': all_cites,
#                  'all_types': all_types,
#                  'all_cats': all_cats,
#                  'down_cats': down_cats,
#                  'up_cats': up_cats,
#                  'questions': questions,
#                  'show_help': show_help,
#                  'show_hiv': show_hiv,
#                  'show_relapse': show_relapse,
#                  })


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
        org_form = OrgForm(request.POST)
        ServFormset = inlineformset_factory(
            Organizations,
            OrganizationServices,
            exclude=[]
        )
        if org_form.is_valid():
            new_org = org_form.save(commit=False)
            new_org.slug = request.POST['title']
            formset = ServFormset(request.POST, instance=new_org)
            if formset.is_valid():
                new_org.save()
                formset.save()
                return HttpResponse('kkk')
        else:
            return HttpResponse(1341)
    else:
        form = OrgForm()
        OrgFomset = inlineformset_factory(
            Organizations,
            OrganizationServices,
            exclude=(),
            extra=5,
            can_delete=False
        )
        formset = OrgFomset()
        return render(
            request,
            template_name='add_new_org.html',
            context={
                'form': form,
                'formset': formset,
            }
        )
