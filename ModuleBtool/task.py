from flask import request
from QyeryClass.Mongodb import QueryMongo
import json
from bson.objectid import ObjectId
from ModuleBtool.analizations import task_analization
from datetime import datetime


#TODO:тут начинается боль
def create_task(rule):
    response = {'response': 'Pleas enter correct URL'}
    if rule == 'auto':
        date_appearence, content = task_analization.main(request.args.get('content'))
    elif rule == 'manually':
        date_appearence = request.args.get('date_executions')
        content  = request.args.get('content')
    else:
        return json.dumps(response)
    if QueryMongo(collection_type=request.args.get('table_name'),
                  data={
                          'date_appearance': datetime.now(),
                          'date_executions': date_appearence,
                          'completed': False,
                          'content_task': [{
                              'type': request.args.get('type'),
                              'content': content
                          }]}).insert():
        response['response'] ='success'
    return json.dumps(response)
#TODO:тут заканчивается боль


def complete_task():
    response = {'response': 'error'}
    if QueryMongo(collection_type=request.args.get('table_name'),
                  data={'_id': ObjectId(request.args.get('id'))},
                  update_data={'$set': {'completed': request.args.get('result')}}).update():
        response['response'] = 'success'
    return json.dumps(response)


def edit_task():
    response = {'response': 'error'}
    if QueryMongo(collection_type=request.args.get('table_name'),
                  data={'_id': ObjectId(request.args.get('id'))},
                  update_data={'$set':{
                      request.args.get('key'):request.args.get('value')
                  }}).update():
        response['response'] = 'success'
    return json.dumps(response)


def delete_task():
    response = {'response': 'error'}
    if QueryMongo(collection_type=request.args.get('table_name'),
                  data={'_id': ObjectId(request.args.get('id'))}).delete():
        response['response'] = 'success'
    return json.dumps(response)


def check_success_task():
    response = {'response': 'Pleas enter correct URL'}
    in_progress = 0
    failed = 0
    done = 0
    all_task = 0
    for item in QueryMongo(collection_type=request.args.get('table_name')).select():
        if request.args.get('start') <= item['date_execution'] <= request.args.get('finish') \
                or request.args.get('start') <= item['date_appearance'] <= request.args.get('finish'):
            all_task += 1
            if item['completed'] == 'in_progress':
                in_progress += 1
            if item['completed'] == 'failed':
                failed += 1
            if item['completed'] == 'done':
                done += 1
    response['percent_in_progress'] = percent(all_task, in_progress)
    response['percent_failed'] = percent(all_task, failed)
    response['percent_done '] = percent(all_task, done)
    response['response'] = 'success'
    return json.dumps(response)


def percent(all_task, x):
    return x/all_task * 100
