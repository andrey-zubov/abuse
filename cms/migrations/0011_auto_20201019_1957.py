# Generated by Django 3.0 on 2020-10-19 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_articlepicture_newspage_richtextcontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspage',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='richtextcontent',
            name='parent',
        ),
        migrations.DeleteModel(
            name='ArticlePicture',
        ),
        migrations.DeleteModel(
            name='NewsPage',
        ),
        migrations.DeleteModel(
            name='RichTextContent',
        ),
    ]
