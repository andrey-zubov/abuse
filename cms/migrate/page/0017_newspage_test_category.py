# Generated by Django 3.0 on 2020-10-19 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0016_auto_20201019_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspage',
            name='test_category',
            field=models.CharField(choices=[('no', 'Без располажение в header-е'), ('down', 'Нижний header'), ('up', 'Верхний header')], default=1, max_length=64),
            preserve_default=False,
        ),
    ]
