# Generated by Django 3.0 on 2020-10-20 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0026_auto_20201019_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepicture',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articlepicture_set', to='page.NewsPage'),
        ),
        migrations.AlterField(
            model_name='newspage',
            name='template_key',
            field=models.CharField(choices=[('widgets/news_widget.html', 'Новость')], default='widgets/news_widget.html', max_length=255, verbose_name='template'),
        ),
        migrations.AlterModelTable(
            name='articlepicture',
            table='page_newspage_articlepicture',
        ),
    ]