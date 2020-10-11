# -*- coding: utf-8 -*-
import json
from loguru import logger

NAME = None
TOKEN = None
LAST_REPLY_MESSAGE = None
ADD_PERSON = False
REMOVE_PERSON = False
TIMEZONE = 'Europe/Moscow'
TIMEZONE_COMMON_NAME = 'Moscow'

numbers = [-1, 1, 2, 3, 5, 10]
trust_list = ['ristleell', 'Barzello', 'ra3vld', 'Agamayunov']
girls = ['Тома', 'Соня']

with open('key.json', encoding='utf-8') as key:
    keys = json.load(key)
    TOKEN = keys["telegram"]


@logger.catch
def load_beer_list():
    data = None
    with open('../data/beer.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return data


@logger.catch
def save_beer_list(js):
    with open("../data/beer.json", 'w', encoding='utf8') as json_file:
        json.dump(js, json_file, ensure_ascii=False)
