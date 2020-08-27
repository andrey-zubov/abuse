from django.urls import path, include
from .views import main_page, articles_by_cat, org_info, news_view, add_new_org

urlpatterns = [
    path('abuse/', main_page),
    path('abuse/organization/<slug>', org_info, name='org_info'),
    path('abuse/news/', news_view),
    path('abuse/add_organization', add_new_org),

    path('abuse/<slug>/', articles_by_cat, name='main_articles'),

]