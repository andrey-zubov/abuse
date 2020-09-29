from django.contrib import admin
from .models import (
    Link,
    Organizations,
    ServicesType,
    OrganizationServices,
    City,
    Question,
    Answer,
    Choice,
    HelpFile,
    FAQ,
    FAQlist,
    Vacancy,
    Event,
    Partner,
    Region,
    Area
)


class ServicesAdmin(admin.StackedInline):
    model = OrganizationServices
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [ServicesAdmin]
    prepopulated_fields = {'slug': ('title',), }


class ChoicesAdmin(admin.StackedInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoicesAdmin]


class FAQinline(admin.StackedInline):
    model = FAQlist
    extra = 1


class FAQAdmin(admin.ModelAdmin):
    inlines = [FAQinline]

admin.site.register(Link)
admin.site.register(Organizations, OrganizationAdmin)


admin.site.register(City)
admin.site.register(ServicesType)

admin.site.register(HelpFile)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

admin.site.register(Vacancy)
admin.site.register(Event)

admin.site.register(FAQ, FAQAdmin)

admin.site.register(Partner)

admin.site.register(Region)
admin.site.register(Area)
