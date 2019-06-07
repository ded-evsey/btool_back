from flask import request
import json


#TODO:тут начинается боль
def create_task(type):
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    table_name = ''
    if request.args.get('table_type') == 'group':
        table_name = '_g'+request.args.get('id')
    elif request.args.get('table_type') == 'user':
        table_name = '_u'+request.args.get('id')
    if type == 'auto':
        print('auto', table_name)
    elif type == 'manually':
        print('manual', table_name)
    return json.dumps(response)
#TODO:тут заканчивается боль


def complete_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


def edit_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


def delete_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


def check_success_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)
