from .models import *
import codecs
from transliterate import translit
import pandas as pd
import numpy as np
import pickle


def fill_db(request=None):
    file = codecs.open('init_org.txt', encoding='utf-8', mode='r')
    text = file.readlines()
    buffer = {}
    orgs = []
    pre_city = City.objects.latest('id')
    for line in text:
        if line[:3] != '---':
            s = line.split(':', 1)
            if len(s) == 1:
                continue
            buffer[s[0]] = s[1]
        else:
            orgs.append(buffer)
            buffer = {}
    for i in orgs:
        #     pre_city = 1
        title = i['организация'] if i['организация'] else ''
        try:
            adress = i['адресс']
        except:
            adress = ''

        try:
            desctiption = i['описание']
        except:
            desctiption = ''

        try:
            working_hours = i['время работы']
        except:
            working_hours = ''

        try:
            tel1 = i['тел1']
        except:
            tel1 = ''

        try:
            tel2 = i['тел2']
        except:
            tel2 = ''

        try:
            tel3 = i['тел3']
        except:
            tel3 = ''

        try:
            website = i["сайт"]
        except:
            website = ''
        try:
            email = i['email']
        except:
            email = ''
        pre_slug = title
        pre_slug = pre_slug.replace(' ', '_')[:31].replace(',', '').replace('.', '').replace(':', '').replace(';', '').replace('!', '').replace('"', '').replace("'", '').replace('?', '').replace('/', '').replace('|', '').replace('«', '').replace('»', '').replace('(', '').replace(')', '')
        pre_slug = translit(pre_slug, 'ru', reversed=True)
        slug = check_slug(pre_slug)
        Organizations.objects.create(city=pre_city, title=title, slug=slug, adress=adress, desctiption=desctiption,
                                     working_hours=working_hours, tel1=tel1, tel2=tel2, tel3=tel3, website=website,
                                     email=email)

    return 'done organizations import'


def check_slug(slug):
    if Organizations.objects.filter(slug=slug).exists():
        slug += '1'
        return check_slug(slug)
    else:
        return slug


def fill_regions(request=None):
    with open('output_data.txt', 'rb') as f:
        data = pickle.load(f)

    for reg in data:
        new_reg = Region.objects.create(title=reg)
        for area in data[reg]:
            new_area = Area.objects.create(title=area, region=new_reg)

    return 'done regions and areas import'




