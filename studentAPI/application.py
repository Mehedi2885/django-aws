from django.http import request
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/'
ENDPOINT = 'api/'


def get_resource(name=None):
    data = {}
    if name is not None:
        data = {
            'name': name
        }
    resp = requests.get(BASE_URL + ENDPOINT, data=json.dumps(data))
    print(resp.status_code)
    print(resp.json())


def post_resource():
    new_std = {
        'name': 'Aqsa Hassan',
        'rollNo': 7,
        'marks': 100,
        'subjects': 'history',
    }
    resp = requests.post(BASE_URL + ENDPOINT, data=json.dumps(new_std))
    print(resp.status_code)
    print(resp.json())


def update_resource(id):
    new_data = {
        'id': id,
        'name': 'Ayat Hassan',
        'subjects': 'Software Engineering',
    }
    resp = requests.put(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    print(resp.status_code)
    print(resp.json())


def delete_resource(id=None):
    data = {
        'id': id,
    }
    resp = requests.delete(BASE_URL + ENDPOINT, data=json.dumps(data))
    print(resp.status_code)
    print(resp.json())


get_resource('M')
#post_resource()
# update_resource(4)
#delete_resource()