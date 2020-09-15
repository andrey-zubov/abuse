from django.forms import ModelForm, BaseInlineFormSet
from .models import Organizations, OrganizationServices, Vacancy


class OrgForm(ModelForm):
    class Meta:
        model = Organizations
        exclude = ['slug', 'city', 'vacancies']


# class OrgServsForm(ModelForm):
#     class Meta:
#         model = OrganizationServices
#         exclude = []

class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['city']
