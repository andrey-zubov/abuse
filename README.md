  * Установка работающей feincms:
  > pip install feincms
  > pip uninstall django
  > pip install django==3.0

  * Примечание - django 3.0 это версия, с которой feincms работает корректно.feincms

  * Для корректной работы нужно сделать миграции приложений page и medialibrary (см settings INSTALLED_APPS)
  * Миграции этих приложений лежат / будут генерироваться в папке cms/migrate (настроено в settings MIGRATION_MODULES)
  * В случае если миграций в cms/migrate нет делать:
    > python manage.py makemigrations page
    > python manage.py makemigrations medialibrary
    > python manage.py makemigrations
    > python manage.py migrate

  * feincms требует статику:
   > python manage.py collectstatic

  * Документция feincms:
   > https://feincms-django-cms.readthedocs.io/en/latest/





