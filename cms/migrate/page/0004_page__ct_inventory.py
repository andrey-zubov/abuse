# Generated by Django 3.0 on 2020-10-05 16:45

from django.db import migrations
import feincms.contrib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_auto_20200929_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='_ct_inventory',
            field=feincms.contrib.fields.JSONField(blank=True, editable=False, null=True, verbose_name='content types'),
        ),
    ]