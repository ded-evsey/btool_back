from flask import request
from QyeryClass.Mongodb import QueryMongo
import datetime
import json
from bson.objectid import ObjectId
from ModuleBtool.analizations import sentimental


def send_message():
    response = {'response': 'error'}
    message = QueryMongo(collection_type=request.args.get('table_name'),
                         data={'from_id': request.args.get('from_id'),
                               'to_id': request.args.get('to_id'),
                               'datetime': datetime.datetime.now(),
                               'content_message': [
                                   {'type': request.args.get('type'),
                                    'content': request.args.get('content')}]}).insert()
    print(message)
    if message:
        response['response'] = 'success'
    return json.dumps(response)


def rewrite_message():
    response = {'response': 'error'}
    if QueryMongo(name_collection=request.args.get('table_name'),
                  data={'_id': ObjectId(request.args.get('id'))},
                  update_data={'$set': {'message_content': [
                      {'content': request.args.get('new_content')}]}}).update():
        response['response'] = 'success'
    return json.dumps(response)


def delete_message():
    response = {'response': 'error'}
    message = QueryMongo(collection_type=request.args.get('table_name'), data={'_id': ObjectId(request.args.get('id'))})
    if message:
        response['response'] = 'success'
    return json.dumps(response)


def show_message():
    response = {'response': 'error'}
    messages = ''
    for item in QueryMongo(collection_type=request.args.get('table_name'),
                           query_type=0).select():
        messages += str(item)
    if messages:
        response['response'] = 'success'
        response['messages'] = messages
    return json.dumps(response)


def sentimental_analysis_group():
    response = {'response': 'error'}
    list_massage = []
    for item in QueryMongo(collection_type='message_box_g', name_collection=request.args.get('id')).select():
        if item['content_message']['type'] == 'text':
            list_massage.append(item['content_message']['content'])
    if list_massage:
        response['response'] = 'success'
        response['result'] = sentimental.main(list_massage)

    return json.dumps(response)
