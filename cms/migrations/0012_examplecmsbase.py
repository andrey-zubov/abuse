# Generated by Django 3.0 on 2020-10-19 17:24

from django.db import migrations, models
import feincms.extensions.base


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20201019_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleCMSBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, feincms.extensions.base.ExtensionsMixin),
        ),
    ]
