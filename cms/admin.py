from django.contrib import admin
from .models import Articles, Link, Block, Main_Cat

admin.site.register(Articles)
admin.site.register(Link)
admin.site.register(Block)
admin.site.register(Main_Cat)

# Register your models here.
