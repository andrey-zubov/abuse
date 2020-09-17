from django.forms import ModelForm, BaseInlineFormSet
from .models import (
    Organizations,
    Vacancy,
    Event
)


class OrgForm(ModelForm):
    class Meta:
        model = Organizations
        exclude = ['slug', 'city', 'vacancies']


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['city']


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['city']
