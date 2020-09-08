from django.contrib import admin
from .models import (
    Articles,
    Link,
    Block,
    Main_Cat,
    Organizations,
    ServicesStuff,
    ServicesType,
    ServicesConf,
    ServicesPayment,
    OrganizationServices,
    City,
    PageType,
    NewsSource,
    Question,
    Answer,
    Choice
)


class ServicesAdmin(admin.StackedInline):
    model = OrganizationServices
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [ServicesAdmin]
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Articles)
admin.site.register(Link)
admin.site.register(Block)
admin.site.register(Main_Cat)
admin.site.register(Organizations, OrganizationAdmin)


admin.site.register(City)
admin.site.register(ServicesType)
admin.site.register(ServicesConf)
admin.site.register(ServicesPayment)
admin.site.register(ServicesStuff)

admin.site.register(PageType)
admin.site.register(NewsSource)

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Choice)

# Register your models here.
