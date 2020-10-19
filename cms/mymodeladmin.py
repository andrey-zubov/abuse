from __future__ import absolute_import, unicode_literals

from threading import local

from django.utils.translation import gettext_lazy as _

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

try:
    from django.contrib.staticfiles.templatetags.staticfiles import static
except ImportError:
    # Newer Django versions.
    from django.templatetags.static import static

from feincms.admin import item_editor
from feincms.module.page.modeladmins import PageAdmin

#  this is feincms PageAdmin class with modified fieldsets. Needed to resolve unique fields conflict
class MyPageAdmin(PageAdmin):
    fieldsets = [
        (None, {"fields": [("title", "slug"), ("active", "in_navigation")]}),
        (
            _("Other options"),
            {
                "classes": ["collapse"],
                "fields": ["template_key", "parent", "override_url", "redirect_to"],
            },
        ),
        # <-- insertion point, extensions appear here, see insertion_index
        # above
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]
