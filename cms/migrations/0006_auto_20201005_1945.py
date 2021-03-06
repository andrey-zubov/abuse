# Generated by Django 3.0 on 2020-10-05 16:45

from django.db import migrations, models
import django.db.models.deletion
import feincms.module.medialibrary.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_page__ct_inventory'),
        ('medialibrary', '0001_initial'),
        ('cms', '0005_auto_20200929_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizations',
            name='picture',
            field=feincms.module.medialibrary.fields.MediaFileForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medialibrary.MediaFile', verbose_name='Картинка'),
        ),
        migrations.CreateModel(
            name='OrgTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_help', models.BooleanField(default=True, verbose_name='Первая помощь')),
                ('side_links', models.ManyToManyField(blank=True, to='page.Page')),
            ],
            options={
                'verbose_name': 'Шаблон страницы организаций',
                'verbose_name_plural': 'Шаблон страницы организаций',
            },
        ),
    ]
