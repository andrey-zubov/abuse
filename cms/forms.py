from django.forms import ModelForm, BaseInlineFormSet
from .models import Organizations, OrganizationServices


class OrgForm(ModelForm):
    class Meta:
        model = Organizations
        exclude = ['slug', 'city', 'vacancies']


class OrgServsForm(ModelForm):
    class Meta:
        model = OrganizationServices
        exclude = []

