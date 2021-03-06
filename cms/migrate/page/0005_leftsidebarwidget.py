# Generated by Django 3.0 on 2020-10-18 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_page__ct_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeftSidebarWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('show_help', models.BooleanField(default=False, verbose_name='Отображать "первая помощь')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текстовая информация')),
                ('left_link', models.ManyToManyField(blank=True, related_name='left_sidebar_link', to='page.Page')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leftsidebarwidget_set', to='page.Page')),
            ],
            options={
                'verbose_name': 'Левый сайдбар',
                'verbose_name_plural': 'Левый сайдбар',
                'db_table': 'page_page_leftsidebarwidget',
                'ordering': ['ordering'],
                'permissions': [],
                'abstract': False,
            },
        ),
    ]
