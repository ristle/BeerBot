# -*- coding: utf-8 -*-
import json

NAME = None
TOKEN = None
LAST_REPLY_MESSAGE = None
ADD_PERSON=False
TIMEZONE = 'Europe/Moscow'
TIMEZONE_COMMON_NAME = 'Moscow'

numbers = [1, 2, 3, 5, 10]
trust_list = ['ristleell', 'Barzello', 'ra3vld']
girls = ['Тома', 'Соня']

with open('key.txt', 'r') as file:
    TOKEN = file.read()

def load_beer_list():
    data = None
    with open('../data/beer.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return data

def save_beer_list(js):
    with open("../data/beer.json", 'w', encoding='utf8') as json_file:
        json.dump(js, json_file, ensure_ascii=False)
