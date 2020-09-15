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
    'title': _('Новость'),
    'path': 'widgets/base_widget.html',
    'regions': (
        ('main', _('Main content area')),
    ),
})


Page.register_templates({
    'title': _('Отдельная статья'),
    'path': 'widgets/single_article.html',
    'regions': (
        ('main', _('Main content area')),
    ),
})

Page.create_content_type(RichTextContent)

# class OrgWidget(models.Model):
#     class Meta:
#         abstract = True
#
#     def render(self):
#         orgs = Organizations.objects.all().prefetch_related('organizationservices_set')
#         all_cites = City.objects.filter()
#         all_types = ServicesType.objects.filter()
#         return render_to_string(
#             'widgets/org_widget.html',
#             context={'widget': self,
#                      'orgs': orgs,
#                      'all_cites': all_cites,
#                      'all_types': all_types,
#                      })
#
#
# Page.create_content_type(OrgWidget)


class CalendarArticle(models.Model):
    class Meta:
        abstract = True
    def render(self):
        return render_to_string(
            'widgets/calendar_widget.html',
            context={'widget': self,
                     })

Page.create_content_type(CalendarArticle)


class EmploymentArticle(models.Model):
    class Meta:
        abstract = True

    def render(self):
        all_cityes = City.objects.all()
        vacancies = Vacancy.objects.all()
      #  orgs = Organizations.objects.filter(vacancies=True)
        return render_to_string(
            'widgets/employment_widget.html',
            context={'widget': self,
                     'all_cityes': all_cityes,
                     # 'orgs': orgs,
                     'vacancies': vacancies
                     })


Page.create_content_type(EmploymentArticle)


class AccordeonArticle(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    text = models.TextField(
        null=True,
        blank=True,
        help_text='в формате <p>Текст пункта</p>'
    )

    def render(self):
        faq = FAQ.objects.all()
        return render_to_string(
            'widgets/accordeon_widget.html',
            context={'widget': self,
                     'faq':faq
                     })


Page.create_content_type(AccordeonArticle)


class ArticlePicture(models.Model):
    class Meta:
        abstract = True

    picture = MediaFileForeignKey(
        MediaFile,
        on_delete=models.SET_NULL,
        verbose_name='Картинка',
        null=True,
        blank=True,
    )

    def get_img(self):
        return join(settings.MEDIA_URL, str(self.picture.file))

    def render(self):
        return render_to_string(
            'widgets/picture_widget.html',
            context={'widget': self})


Page.create_content_type(ArticlePicture)


class Vacancy(models.Model):
    title = models.CharField(
        max_length=256,
    )
    desctiption = models.TextField()
    time = models.CharField(
        choices=[
            ('1', 'Полная занятость'),
            ('2', 'Частичная занятость'),
            ('3', 'Подработка'),
            ('4', 'Гибкий график'),
        ],
        max_length=64
    )
    ownership = models.CharField(
        choices=[
            ('1', 'Государственная'),
            ('2', 'Комерческая'),
            ('3', 'Общественная организация'),
            ('4', 'Религиозная организация'),
        ],
        max_length=64
    )
    employer = models.CharField(
        max_length=256,
    )
    tel = models.CharField(
        max_length=30
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    )
    adress = models.TextField()
    position = models.CharField(
        max_length=256
    )
    org_employer = models.CharField(
        max_length=256
    )
    email = models.EmailField()


class FAQ(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='пункт FAQ'
    )


class FAQlist(models.Model):
    article = models.ForeignKey(
        FAQ,
        on_delete=models.CASCADE,
    )
    title = models.TextField(
        verbose_name='Заголовок статьи'
    )
    text = models.TextField(
        verbose_name='Содержимое статьи'
    )


class Link(models.Model):
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    title = models.CharField(
        verbose_name='Назание ссылки',
        help_text='Будет отображаться на кнопке',
        max_length=256
    )
    link = models.CharField(
        max_length=1024,
        verbose_name='ссылка',
        help_text='Для навигации',
    )
    info = models.CharField(
        verbose_name='Описание',
        null=True,
        blank=True,
        max_length=50
    )

    def __str__(self):
        if self.info:
            return self.info
        else:
            return self.title


class HelpFile(models.Model):
    file = models.FileField(
        verbose_name='Файл',
        null=True,
        blank=False
    )

    @property
    def get_file(self):
        return join(settings.MEDIA_URL, str(self.file.file))

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
    # employment_widget = models.BooleanField(
    #     verbose_name='Отображать виджет трудоустройство'
    # )
    org_widget = models.BooleanField(
        verbose_name='Отображать виджет организаций'
    )
    cross_link = models.ManyToManyField(
        'self',
        null=True,
        blank=True
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
        max_length=32
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


class ArticleCategory(Extension):
    def handle_model(self):
        self.model.add_to_class(
            'category',
            models.ManyToManyField(
                Main_Cat,
                null=False,
                blank=False

            )
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(
            _("Категория"),
            {"fields": ("category",), },
        )


Page.register_extensions(ArticleCategory)


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


class LinkExtension(Extension):
    def handle_model(self):
        self.model.add_to_class(
            'button',
            models.ManyToManyField(
                Link,
                verbose_name='Ссылка под статьей',
                null=True,
                blank=True,
            )
        )
        self.model.add_to_class(
            'org_button',
            models.BooleanField(
                default=False,
                verbose_name='Отображать кнопку быстрого перехода к организациям'
            )
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(
            _("Кнопки"),
            {"fields": ("button", "org_button",), },
        )

Page.register_extensions(LinkExtension)

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

