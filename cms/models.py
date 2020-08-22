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
    'path': 'widgets/base_widget.html',
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
    class Meta:
        verbose_name = 'Одноколоночный'
        abstract = True

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



    def render(self):
        return render_to_string(
            'singlecolumn_article.html',
            context={
                'widget': self,
                'text': mark_safe(self.text)
            })

    def get_img(self):
        if not self.picture:
            return None
        else:
            return join(settings.MEDIA_URL, str(self.picture.file))

Page.create_content_type(Column)

class Articles(models.Model):
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    category = models.ManyToManyField('Main_Cat')
    is_active = models.BooleanField(default=True)
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
    points = models.TextField(
        verbose_name='Пункты/список',
        blank=True,
        null=True,
        help_text='<li> текст пункта </li>'
    )
    link = models.ManyToManyField(
        'Link',
        null=True,
        blank=True,
        verbose_name='Ссылка',
        help_text='Можно добавить ардесс-ссылку на внешний источник или'
                  ' на статью.'
    )

    def get_img(self):
        if not self.picture:
            return None
        else:
            return join(settings.MEDIA_URL, str(self.picture.file))

    def __str__(self):
        return self.title


class Link(models.Model):
    link = models.URLField(
        verbose_name='ссылка'
    )
    title = models.CharField(
        verbose_name='Назание ссылки',
        max_length=256
    )


class Block(models.Model):  # Todo REFACTOR
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, verbose_name="Название блока")
    slug = models.SlugField(verbose_name="Слаг")
    name_button = models.CharField(
        max_length=100,
        verbose_name="Название кнопки",
        null=True,
        blank=True
    )
    text = models.TextField(verbose_name="Текст блока")
    picture = MediaFileForeignKey(MediaFile,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  verbose_name="Картинка")
    # categories = models.ManyToManyField(Category, verbose_name="Раздел-категория-тег")
    pages = models.ManyToManyField(Page, verbose_name="Статьи")

    def get_img(self):
        if not self.picture:
            return None
        else:
            return join(settings.MEDIA_URL, str(self.picture.file))


class Main_Cat(models.Model):
    class Meta:
        verbose_name = 'Главные категории'
        verbose_name_plural = 'Главные категории'

    header_choices = [
        ('up', 'Верхний header'),
        ('down', 'Нижний header')
    ]

    is_active = models.BooleanField(default=True)
    header_menu = models.CharField(
        verbose_name='Местоположение',
        choices=header_choices,
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='слаг',
        null=True,
        blank=True
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=50
    )

    def __str__(self):
        return self.title


class Organizations(models.Model):
    title = models.CharField(
        verbose_name='Название организации',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )
    working_hours = models.CharField(
        verbose_name='Время работы',
        max_length=50,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        'City',
        verbose_name='Город',
        on_delete=models.DO_NOTHING
    )
    adress = models.CharField(
        verbose_name='адресс',
        max_length=256,
        null=True,
        blank=True
    )
    desctiption = models.TextField(
        verbose_name="описание",
        null=True,
        blank=True
    )
    tel1 = models.CharField(
        verbose_name='Телефон',
        null=True,
        blank=True,
        max_length=16
    )
    tel2 = models.CharField(
        verbose_name='Телефон',
        null=True,
        blank=True,
        max_length=16
    )
    tel3 = models.CharField(
        verbose_name='Телефон',
        null=True,
        blank=True,
        max_length=16
    )
    website = models.URLField(
        verbose_name='Сайт',
        null=True,
        blank=True
    )
    email = models.EmailField(
        verbose_name='электронная почта',
        null=True,
        blank=True
    )

    @property
    def get_services(self):
        return self.organizationservices_set.all()

    def __str__(self):
        return self.title


class City(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Город'
    )
    def __str__(self):
        return self.title


class OrganizationServices(models.Model):
    organization = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
    )
    org_type = models.ForeignKey(
        'ServicesType',
        on_delete=models.DO_NOTHING,
    )
    stuff = models.ForeignKey(
        'ServicesStuff',
        on_delete=models.DO_NOTHING,
    )
    conf = models.ForeignKey(
        'ServicesConf',
        on_delete=models.DO_NOTHING,
    )
    payment = models.ForeignKey(
        'ServicesPayment',
        on_delete=models.DO_NOTHING,
    )


class ServicesType(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title


class ServicesStuff(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title


class ServicesConf(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title


class ServicesPayment(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title
