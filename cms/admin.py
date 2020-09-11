from django.contrib import admin
from .models import (
    Articles,
    Link,
    Main_Cat,
    Organizations,
    ServicesStuff,
    ServicesType,
    ServicesConf,
    ServicesPayment,
    OrganizationServices,
    City,
    Question,
    Answer,
    Choice,
    HelpFile
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



admin.site.register(Articles)
admin.site.register(Link)
admin.site.register(Main_Cat)
admin.site.register(Organizations, OrganizationAdmin)


admin.site.register(City)
admin.site.register(ServicesType)
admin.site.register(ServicesConf)
admin.site.register(ServicesPayment)
admin.site.register(ServicesStuff)

admin.site.register(HelpFile)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

# Register your models here.
