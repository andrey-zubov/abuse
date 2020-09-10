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
from feincms.extensions import Extension

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
    button_orgs = models.BooleanField(
        verbose_name='Добавить кнопку-переход к организациям',

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
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    info = models.CharField(
        verbose_name='Описание',
        null=True,
        blank=True,
        max_length=50
    )

    link = models.URLField(
        verbose_name='ссылка',
        help_text='Для навигации',
    )
    title = models.CharField(
        verbose_name='Назание ссылки',
        help_text='Будет отображаться на кнопке',
        max_length=256
    )


    def __str__(self):
        if self.info:
            return self.info
        else:
            self.title


# class Block(models.Model):  # Todo REFACTOR
#     is_active = models.BooleanField(default=True)
#     title = models.CharField(max_length=100, verbose_name="Название блока")
#     slug = models.SlugField(verbose_name="Слаг")
#     name_button = models.CharField(
#         max_length=100,
#         verbose_name="Название кнопки",
#         null=True,
#         blank=True
#     )
#     text = models.TextField(verbose_name="Текст блока")
#     picture = MediaFileForeignKey(MediaFile,
#                                   on_delete=models.SET_NULL,
#                                   null=True,
#                                   blank=True,
#                                   verbose_name="Картинка")
#     # categories = models.ManyToManyField(Category, verbose_name="Раздел-категория-тег")
#     pages = models.ManyToManyField(Page, verbose_name="Статьи")
#
#     def get_img(self):
#         if not self.picture:
#             return None
#         else:
#             return join(settings.MEDIA_URL, str(self.picture.file))


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
    help_widget = models.BooleanField(
        verbose_name='Отображать виджет "первая помощь"'
    )
    hiv_widget = models.BooleanField(
        verbose_name='Отображать виджет "вич и гепатит"'
    )
    relapse_widget = models.BooleanField(
        verbose_name='Отображать виджет "срыв"'
    )

    org_widget = models.BooleanField(
        verbose_name='Отображать виджет организаций'
    )

    def __str__(self):
        return self.title


class Organizations(models.Model):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

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
    class Meta:
        verbose_name = 'Вид деятельности'
        verbose_name_plural = 'Виды деятельности'

    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title


class ServicesStuff(models.Model):
    class Meta:
        verbose_name = 'Вещество'
        verbose_name_plural = 'Вещества'

    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title


class ServicesConf(models.Model):
    class Meta:
        verbose_name = 'Конфиденциальнось'
        verbose_name_plural = 'Конфиденциальнось'

    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title


class ServicesPayment(models.Model):
    class Meta:
        verbose_name = 'Оплата услуг'
        verbose_name_plural = 'Оплата услуг'

    title = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.title


class TypeExtension(Extension):
    def handle_model(self):
        self.model.add_to_class(
            'type',
            models.BooleanField(
                verbose_name='Является новостью',
                default=True
            )
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(
            _("Тип статьи"),
            {"fields": ("type",), },
        )

Page.register_extensions(TypeExtension)


class NewsImageExtension(Extension):
    def handle_model(self):
        self.model.add_to_class(
            'preview_img',
            MediaFileForeignKey(
                MediaFile,
                on_delete=models.SET_NULL,
                verbose_name='Выбрать картинку',
                null=True,
                blank=True,
            )
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(
            _("Выбрать картинку на превью"),
            {"fields": ("preview_img",), },
        )


Page.register_extensions(NewsImageExtension)


class NewsSourceExtension(Extension):
    def handle_model(self):
        self.model.add_to_class(
            'source',
            models.CharField(
                verbose_name='Ссылка на источник',
                max_length=256,
                null=True,
                blank=True
            )
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(
            _("Ссылка на источник"),
            {"fields": ("source",), },
        )


Page.register_extensions(NewsSourceExtension)


# опросник
class Question(models.Model):
    title = models.CharField(
        verbose_name='вопрос',
        max_length=150
    )
    is_active = models.BooleanField(
        verbose_name='Опрос активен',
        default=True
    )
    def __str__(self):
        answers = Answer.objects.filter(question=self)
        choices = [i.title for i in self.get_choices()]
        dic = {}
        for ch in choices:
            dic[ch] = answers.filter(choice__title=ch).count()
        return f'{self.title} проголосовало: {answers.count()}. Итоги: {dic}'

    def get_choices(self):
        return self.choice_set.all()


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Вариант для ответа',
        max_length=150
    )
    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.question.title}: {self.choice.title}'

