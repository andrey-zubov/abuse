from django.db import models

from django.utils.translation import gettext_lazy as _

from feincms.module.page.models import Page
from feincms.contents import RichTextContent
from feincms.module.medialibrary.contents import MediaFileContent

Page.register_extensions(
    'feincms.extensions.datepublisher',
    'feincms.extensions.translations'
)  # Example set of extensions

Page.register_templates({
    'title': _('Standard template'),
    'path': 'test_page.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
    ),
})

Page.create_content_type(RichTextContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('lightbox', _('lightbox')),
))