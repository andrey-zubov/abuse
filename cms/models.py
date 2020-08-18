from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.safestring import mark_safe

from os.path import join

from feincms.module.page.models import Page
from feincms.contents import RichTextContent
from feincms.module.medialibrary.contents import MediaFileContent
from feincms.module.medialibrary.fields import MediaFileForeignKey, MediaFile

from mptt import register
from mptt.models import MPTTModel, TreeForeignKey

Page.register_extensions(
    'feincms.extensions.datepublisher',
    'feincms.extensions.translations'
)  # Example set of extensions

Page.register_templates({
    'title': _('Standard template'),
    'path': 'base_0.html',
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


class Column(models.Model):
    title = models.CharField(
        verbose_name='Название виджета',
        max_length=256,
    )
    picture = MediaFileForeignKey(
        MediaFile,
        on_delete=models.SET_NULL,
        verbose_name='Картинка',
        null=True,
    )
    pic_text = models.CharField(
        verbose_name='Подпись катринки',
        max_length=256
    )
    text = models.TextField(
        verbose_name='основной текст',
    )

    class Meta:
        verbose_name = 'Одноколоночный'
        abstract = True

    def render(self):
        return render_to_string(
            'main_article.html',
            context={
                'widget': self,
                'text': mark_safe(self.text)
            })

    def get_img(self):
        return join(settings.MEDIA_URL, str(self.picture.file))

Page.create_content_type(Column)

class where_find_help(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    picture = MediaFileForeignKey(
        MediaFile,
        on_delete=models.SET_NULL,
        verbose_name='Картинка',
        null=True,
        blank=True,
    )
    pic_text = models.CharField(
        verbose_name='Подпись катринки',
        max_length=256,
        null=True,
        blank=True
    )
    text = models.TextField(
        verbose_name='основной текст',
    )
    href = models.ForeignKey(
        'Link',
        verbose_name='Ссылка',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Link(models.Model):
    link = models.URLField(
        verbose_name='ссылка'
    )
    title = models.CharField(
        verbose_name='Назание ссылки',
        max_length=256
    )
