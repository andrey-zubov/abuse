from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.safestring import mark_safe
import datetime


from os.path import join

from feincms.module.page.models import Page
from feincms.contents import RichTextContent
from feincms.module.medialibrary.contents import MediaFileContent
from feincms.module.medialibrary.fields import MediaFileForeignKey, MediaFile
from feincms.extensions import Extension

from mptt import register
from mptt.models import MPTTModel, TreeForeignKey

import requests

Page.register_extensions(
    'feincms.extensions.datepublisher',
    'feincms.extensions.translations'
)  # Example set of extensions

Page.register_templates({
    'title': _('Новость'),
    'path': 'widgets/news_widget.html',
    'regions': (
        ('main_news', _('Новость')),
    ),
})

Page.register_templates({
    'title': _('Отдельная статья'),
    'path': 'widgets/refactor_art.html',
    'regions': (
        ('main', _('Статьи')),
        ('sections', _('Нижнии секции')),
        ('right_sidebar', _('Правый сайдбар')),
        ('footer', _('footer')),
    ),
})


Page.create_content_type(RichTextContent, regions=('main_news',))


class StandartArticle(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Стандартная статья'
        verbose_name_plural = 'Стандартные статья'

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    picture = MediaFileForeignKey(
        MediaFile,
        on_delete=models.SET_NULL,
        verbose_name='Картинка',
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текст',
        null=True,
        blank=True)
    list = models.TextField(
        verbose_name='Список',
        null=True,
        blank=True,
        help_text='<li><p>Текст пункта списка</p></li>'
    )
    link = models.ManyToManyField(
        "cms.Link",
        verbose_name='Добавить ссылку',
        null=True,
        blank=True
    )
    org_button = models.BooleanField(
        verbose_name="Ссылка на ближайшие организации"
    )

    def render(self):
        return render_to_string(
            'widgets/standart_article_widget.html',
            context={'widget': self}
        )

    def get_img(self):
        return join(settings.MEDIA_URL, str(self.picture.file))


Page.create_content_type(StandartArticle, regions=('main',))


class CalendarArticle(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Статья с календарем'
        verbose_name_plural = 'Стати с календарем'


    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    text = models.TextField()
    list = models.TextField(
        default='<li></li>',
    )
    bank_link = models.CharField(
        verbose_name='Ссылка на банк вакансий',
        max_length=256,
        null=True,
        blank=True
    )


    def render(self):
        all_cityes = City.objects.all()
        all_events = Event.objects.filter(start_date__range=[datetime.date.today(), '2100-01-01',])
        return render_to_string(
            'widgets/calendar_widget.html',
            context={'widget': self,
                     'all_cityes': all_cityes,
                     'all_events': all_events
                     })

Page.create_content_type(CalendarArticle, regions=('main',))


class ParticipantWidget(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Участники проекта'
        verbose_name_plural = 'Участники проекта'

    title = models.CharField(
        verbose_name='заголовок',
        max_length=256
    )

    def __str__(self):
        return str(self.title)

    def render(self):
        partners = Partner.objects.all()
        return render_to_string(
            'widgets/participant_widget.html',
            context={'widget': self,
                     'partners': partners
                     })


Page.create_content_type(ParticipantWidget, regions=('main',))


class EmploymentArticle(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Трудоустройство'
        verbose_name_plural = 'Трудоустройство'

    title = models.CharField(
        verbose_name='заголовок',
        max_length=256
    )

    text = models.TextField(
        verbose_name='Текст',
        null=True,
        blank=True
    )
    list = models.TextField(
        verbose_name='Список',
        null=True,
        blank=True,
        help_text='<li><p>Текст пункта</p></li>'
    )
    link = models.ManyToManyField(
        "cms.Link",
        verbose_name='Добавить ссылку',
        null=True,
        blank=True
    )

    def render(self):
        all_cityes = City.objects.all()
        vacancies = Vacancy.objects.all()
        return render_to_string(
            'widgets/employment_widget.html',
            context={'widget': self,
                     'all_cityes': all_cityes,
                     # 'orgs': orgs,
                     'vacancies': vacancies
                     })


Page.create_content_type(EmploymentArticle, regions=('main',))


class AccordeonArticle(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Правовая информация'
        verbose_name_plural = 'Правовая информация'

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
    link = models.ManyToManyField(
        "cms.Link",
        verbose_name='Добавить ссылку',
        null=True,
        blank=True
    )


    def render(self):
        faq = FAQ.objects.all()
        return render_to_string(
            'widgets/accordeon_widget.html',
            context={'widget': self,
                     'faq':faq
                     })


Page.create_content_type(AccordeonArticle, regions=('main',))



class ArticlePicture(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображение'

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


Page.create_content_type(ArticlePicture, regions=('main_news',))


class OrgSection(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Секция организаций'
        verbose_name_plural = 'Секция организаций'

    title = 'Организации'

    def render(self):
        article_pages = Page.objects.filter(template_key='widgets/refactor_art.html')
        all_orgs = Organizations.objects.filter(is_active=True).prefetch_related('organizationservices_set')
        all_cites = City.objects.filter()
        all_types = ServicesType.objects.filter()
        all_regions = Region.objects.filter()
        all_areas = Area.objects.filter()

        return render_to_string(
            'widgets/org_section.html',
            context={
                'widget': self,
                'article_pages': article_pages,
                'all_orgs': all_orgs,
                'all_cites': all_cites,
                'all_types': all_types,
                'all_regions': all_regions,
                'all_areas': all_areas,
            })


Page.create_content_type(OrgSection, regions=('sections',))


class FeedbackSection(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Секция обратной связи'

    def render(self):
        return render_to_string(
            'widgets/feedback_section.html',
            context={
                'widget': self,
            })


Page.create_content_type(FeedbackSection, regions=('sections',))


class FooterSection(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'секция Footer'

    def render(self):
        down_cats = Page.objects.filter(test_category='down')
        up_cats = Page.objects.filter(test_category='up')

        return render_to_string(
            'widgets/footer_section.html',
            context={
                'widget': self,
                'down_cats': down_cats,
                'up_cats': up_cats
            })


Page.create_content_type(FooterSection, regions=('footer',))


class Vacancy(models.Model):
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = "Вакансии"

    title = models.CharField(
        max_length=256,
    )
    description = models.TextField()
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
        max_length=64
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    )
    adress = models.TextField()
    position = models.CharField(
        max_length=256
    )
    email = models.EmailField()

    def __str__(self):
        return str(self.title)


class Event(models.Model):
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = "Мероприятия"

    title = models.CharField(
        max_length=256
    )
    start_date = models.DateField()
    start_time = models.CharField(
        max_length=30
    )
    event_type = models.CharField(
        choices=[
            ('1', 'Культурные'),
            ('2', 'Образовательные'),
            ('3', 'Просветительские'),
            ('4', 'Религиозные'),
            ('5', 'Спортивные'),
            ('6', 'Отдых'),
            ('7', 'Профориентация'),
            ('8', 'Тренинги'),
        ],
        max_length=32
    )
    payment = models.CharField(
        max_length=64
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE
    )
    adress = models.TextField()
    organizator = models.TextField()
    description = models.TextField()
    tel = models.CharField(
        max_length=32
    )
    person = models.CharField(
        max_length=64,
        verbose_name="Контактное лицо"
    )

    def __str__(self):
        return str(self.title)


class FAQ(models.Model):
    class Meta:
        verbose_name = 'Пункт правовой инофрмации (FAQ)'
        verbose_name_plural = "Пункты правовой инофрмации (FAQ)"

    title = models.CharField(
        max_length=256,
        verbose_name='пункт FAQ'
    )

    def __str__(self):
        return str(self.title)


class FAQlist(models.Model):
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = "Статьи"

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

    def __str__(self):
        return str(self.title)


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
    target = models.CharField(
        choices = [
            ('', 'Открывать в текущей вкладке'),
            ('_blank', 'Открывать в новой вкладке')
        ],
        max_length=64,
        default=('', 'Открывать в текущей вкладке'),
        blank=True
    )

    def __str__(self):
        if self.info:
            return self.info
        else:
            return self.title


class HelpFile(models.Model):
    class Meta:
        verbose_name = 'Файл первой медицинской помощи'

    file = models.FileField(
        verbose_name='Файл',
        null=True,
        blank=False
    )

    @property
    def get_file(self):
        return join(settings.MEDIA_URL, str(self.file.file))

    def save(self, *args, **kwargs):
        if HelpFile.objects.filter().exists():
            raise ValidationError('Только один PDF-файл можно использовать в качестве помощи')
        else:
            super().save(*args, **kwargs)


class Partner(models.Model):
    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = "Партнеры"

    title = models.CharField(
        verbose_name='Наименование',
        max_length=256
    )
    link = models.URLField(
        verbose_name='Ссылка',
    )
    picture = MediaFileForeignKey(
        MediaFile,
        on_delete=models.SET_NULL,
        verbose_name='Выбрать картинку',
        null=True,
        blank=True,
    )
    def __str__(self):
        return str(self.title)


class Organizations(models.Model):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    is_active = models.BooleanField(
        verbose_name='Действующая организация',
        default=False,
        help_text='Подтвердить после проверки данных организации'
    )
    title = models.CharField(
        verbose_name='Название организации',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )
    picture = MediaFileForeignKey(
        MediaFile,
        on_delete=models.SET_NULL,
        verbose_name='Картинка',
        null=True,
        blank=True,
    )
    working_hours = models.CharField(
        verbose_name='Время работы',
        max_length=128,
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
    lat = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    lng = models.CharField(
        max_length=32,
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
        max_length=64
    )
    tel2 = models.CharField(
        verbose_name='Телефон',
        null=True,
        blank=True,
        max_length=64
    )
    tel3 = models.CharField(
        verbose_name='Телефон',
        null=True,
        blank=True,
        max_length=64
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

    def get_img(self):
        return join(settings.MEDIA_URL, str(self.picture.file))

    def save(self, *args, **kwargs):
        if str(self.city).lower() in str(self.adress).lower():
            location = self.adress
        else:
            location = f'{self.city} {self.adress}'
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        google_key = 'AIzaSyAknqsh2KRjjBbPy3V7Cahj1j0M7eDITF0'
        params = {
            'address': location,
            'key': google_key
        }
        r = requests.get(url, params=params)
        results = r.json()['results']
        if results:
            location = results[0]['geometry']['location']
            self.lat, self.lng = location['lat'], location['lng']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Region(models.Model):
    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'

    title = models.CharField(
        max_length=256
    )
    def __str__(self):
        return str(self.title)


class Area(models.Model):
    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=256
    )

    def __str__(self):
        return f'{self.region.title} > {self.title}'


class City(models.Model):
    class Meta:
        verbose_name='Населенный пункт'
        verbose_name_plural='Населенные пункты'
        ordering = ['title']

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Населенный пункт'
    )

    def __str__(self):
        return self.title


class OrganizationServices(models.Model):
    class Meta:
        verbose_name = 'Услуги организации'

    organization = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
    )
    org_type = models.ForeignKey(
        'ServicesType',
        on_delete=models.DO_NOTHING,
        verbose_name='Вид деятельности'
    )
    stuff = models.CharField(
        choices=[
            ('0', 'Не указано'),
            ('1', 'Опиоиды'),
            ('2', 'Психотропы'),
            ('3', 'Галлюциногены'),
        ],
        max_length=64,
        verbose_name="Вещества"
    )
    conf = models.CharField(
        choices=[
            ('0', 'Не указано'),
            ('1', 'Анонимно'),
            ('2', 'Постановка на учет'),
        ],
                max_length=64,
        verbose_name="Конфиденциальность"
    )
    payment = models.CharField(
        choices=[
            ('0', 'Не указано'),
            ('1', 'Платно'),
            ('2', 'Бесплатно'),
        ],
        max_length=64,
        verbose_name="Оплата"
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


class ArticleCategory(Extension):
    def handle_model(self):
        self.model.add_to_class(
            'test_category',
            models.CharField(
                choices=[
                    ('no', 'Без располажение в header-е'),
                    ('down', 'Нижний header'),
                    ('up', 'Верхний header'),
                ],
                max_length=64
            )
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(
            _("Категория"),
            {"fields": ('test_category', ), },
        )


Page.register_extensions(ArticleCategory)


class ArticleSection(Extension):
    def handle_model(self):
        self.model.add_to_class(
            'cross_link',
            models.ManyToManyField(
                Page,
                verbose_name='Ссылки на страницы в левом сайд-баре',
                blank=True
            )
        )
        self.model.add_to_class(
            'show_help',
            models.BooleanField(
                verbose_name='Отображать "первая помощь',
                default=False
            )
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(
            _("Ссылки в левом сайдбаре"),
            {"fields": ('cross_link', 'show_help',), },
        )


Page.register_extensions(ArticleSection)


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
class QuizWidget(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    title = models.CharField(
        verbose_name='Заголовок блока',
        max_length=256,
        null=True,
        blank=True
    )
    text = models.TextField(
        verbose_name='Текстовая информация',
        null=True,
        blank=True
    )

    def render(self):
        quiz = Question.objects.filter(is_active=True)
        return render_to_string(
            'widgets/quiz_widget.html',
            context={
                'widget': self,
                'quiz': quiz
            })


Page.create_content_type(QuizWidget, regions=('right_sidebar',))


class Question(models.Model):
    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

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

    def get_percent(self):
        answers = Answer.objects.filter(question=self)
        choices = [i.title for i in self.get_choices()]
        dic = {}
        for ch in choices:
            answer_amount = answers.filter(choice__title=ch).count()
            if answers.exists():
                answer_percent = round(answer_amount / answers.count() * 100)
            else:
                answer_percent = 0
            dic[ch] = [
                answer_percent,
                answer_amount,
            ]
        return dic

    def get_amount(self):
        answers = Answer.objects.filter(question=self)
        dic = {'all': answers.count()}
        choices = [i.title for i in self.get_choices()]
        for ch in choices:
            dic[ch] = answers.filter(choice__title=ch).count()
        return dic


class Choice(models.Model):
    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

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
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

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


class OrgTemplate(models.Model):
    class Meta:
        verbose_name = 'Шаблон страницы организаций'
        verbose_name_plural = 'Шаблон страницы организаций'

    show_help = models.BooleanField(
        verbose_name='Первая помощь',
        default=True
    )
    side_links = models.ManyToManyField(
        Page,
        blank=True
    )
