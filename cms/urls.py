from django.urls import path, include
from .views import (
    main_page,
    org_info,
    news_view,
    add_new_org,
    help_file,
    megapage,
    faq,
)

urlpatterns = [
    path('abuse/', main_page, name='main_page'),
    path('abuse/organization/<slug>', org_info, name='org_info'),
    path('abuse/news/', news_view, name='news_page'),
    path('abuse/to-partners/', add_new_org, name='to-partners'),
    path('abuse/help', help_file, name='help_pdf'),
    path('abuse/legal-info/', faq, name='faq'),

    path('abuse/<slug>/', megapage, name='main_articles'),

    # path('megapage/<slug>/', megapage, name='articles_page')
]