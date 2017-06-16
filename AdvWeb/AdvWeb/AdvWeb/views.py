# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from AdvWeb import app
from enum import Enum
import os

DEFAULT_CONTENT_KEY = 'home'

DETAILS_DICTIONARY = {'Hebrew': [("טל':", "03-9042273"), ("נייד:", "052-3586954"), ("פקס:", "03-904xxxx")],
                      'Russian': [("Phone:", "03-9042273"), ("CellPhone:", "052-3586954"), ("Fax:", "03-904xxxx")]}

HEBREW_CONTENT_DICTIONARY = {'home': 'home_he.txt', 'about': 'about_he.txt'}
RUSSIAN_CONTENT_DICTIONARY = {'home': 'home_ru.txt'}


class Language(Enum):
    HEBREW = 'Hebrew'
    RUSSIAN = 'Russian'


def get_content(key=None, is_hebrew=True):
    if is_hebrew:
        content_dictionary = HEBREW_CONTENT_DICTIONARY
    else:
        content_dictionary = RUSSIAN_CONTENT_DICTIONARY

    if key is None or content_dictionary.get(key) is None:
        key = DEFAULT_CONTENT_KEY

    path = os.path.join(os.path.dirname(__file__),
                        'static/content/{file_name}'.format(file_name=content_dictionary[key]))
    with open(path, 'rb') as f:
        data = f.readlines()
        for i in xrange(len(data)):
            data[i] = data[i].decode('utf-8')
        return data


def get_details(lang):
    details = DETAILS_DICTIONARY[lang]
    details_content = []
    for key, value in details:
        details_content.append('{key} {value}'.format(key=key, value=value).decode('utf-8'))
    return details_content


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """
        Renders the home page.
    """
    if request.args.get('lang'):
        return home_ru(request.args.get('key'))

    name = 'אינה ציפרסון'.decode('utf-8')
    profession = 'עורכת דין ונוטריון'.decode('utf-8')
    bottom_title = 'צור קשר'.decode('utf-8')

    return render_template('home.html',
                           name=name,
                           date=datetime.strftime(datetime.today(), '%d/%m/%Y'),
                           main_title=name,
                           description_title=name,
                           description_sub_title=profession,
                           main_content=get_content(request.args.get('key')),
                           bottom_title=bottom_title,
                           details=get_details(Language.HEBREW)
                           )


def home_ru(key=None):
    name = 'Inna Tsiperson'.decode('utf-8')
    profession = 'Advocate'.decode('utf-8')
    bottom_title = 'Contact'.decode('utf-8')

    default_content_key = 'home'

    return render_template('HomeRussian.html',
                           name=name,
                           date=datetime.strftime(datetime.today(), '%d/%m/%Y'),
                           main_title=name,
                           description_title=name,
                           description_sub_title=profession,
                           main_content=get_content(key or default_content_key, is_hebrew=False),
                           bottom_title=bottom_title,
                           details=get_details(Language.RUSSIAN)
                           )
