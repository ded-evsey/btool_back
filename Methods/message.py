from flask import request
from QyeryClass.Mongodb import QueryMongo
import datetime
import json
from bson.objectid import ObjectId


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
