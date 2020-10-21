from django.urls import path
from .views import (
    main_page,
    org_info,
    news_view,
    add_new_org,
    help_file,
    create_vac,
    create_event,
    get_answer,
    create_org,
    create_feedback,
    single_news,
)

urlpatterns = [
    path('', main_page, name='main_page'),
    path('organization/<slug>', org_info, name='org_info'),
    path('news/', news_view, name='news_page'),
    path('to-partners/', add_new_org, name='to-partners'),
    path('help', help_file, name='help_pdf'),
    path('create_org/', create_org, name='create_org'),
    path('create_vac/', create_vac, name='create_vacancy'),
    path('create_event/', create_event, name='create_event'),
    path('get_answer/', get_answer, name='get_answer'),
    path('create_feedback', create_feedback, name='create_feedback'),

    path('<slug>', single_news, name='single_news')

]