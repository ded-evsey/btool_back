from flask import request
from PostgreSQL import QueryPg
from Mongodb import QueryMongo
from DBinfo import pg_tables
import datetime
import json
from bson.objectid import ObjectId


def new_group():
    response = {'response': 'error'}
    data = {}
    cr_dict = pg_tables['groups']
    if cr_dict.get('id') !=None :
        cr_dict.pop('id')
    if cr_dict.get('group_contact') !=None :
        cr_dict.pop('group_contact')
    if cr_dict.get('group_message_box') !=None :
        cr_dict.pop('group_message_box')
    for key in cr_dict:
        data[key] = request.args.get(key)
    group_id = QueryPg(table='groups', data=data).insert()
    message_box = QueryMongo(collection_type='message_box_g'+group_id,
                             data={}).insert()
    task_board = QueryMongo(collection_type='task_board_g' + group_id,
                            data={}).insert()
    if message_box and task_board:
        QueryMongo(collection_type='message_box_g' + group_id,
                   data={'_id': ObjectId(message_box)}).delete()
        QueryMongo(collection_type='task_board_g' + group_id,
                   data={'_id': ObjectId(task_board)}).delete()
        response['response'] = 'success'
    return json.dumps(response)


def delete_group():
    response = {'response': 'error'}
    group_id = request.args.get('id')
    group = QueryPg(table='groups', data={'id': group_id}).delete()
    if group > 0:
        message_box = QueryMongo(collection_type='message_box_g' + group_id,
                                 query_type=0).delete()
        task_board = QueryMongo(collection_type='task_board_g' + group_id,
                                query_type=0).delete()
        if message_box and task_board:
            response['response'] = 'success'
    return json.dumps(response)


def update_group():
    response = {'response': 'error'}
    if QueryPg(table='groups',
               data={'id': request.args.get('id'),
                     'new': request.args.get('new')},
               column='name')\
            .update():
        response['response'] = 'success'
    return json.dumps(response)


def new_user_group():
    response = {'response': 'error'}
    data = {}
    for key in pg_tables.values():
        data[key] = request.args.get(key)
    if QueryPg(table='group_contacts_',
               child_name=request.args.get('group_id'),
               data=data).insert():
        response['response'] = 'success'
    return json.dumps(response)


def delete_user_group():
    response = {'response': 'error'}
    if QueryPg(table='group_contacts_',
               child_name=request.args.get('group_id'),
               data={'user_id': request.args.get('user_id')}).delete():
        response['response'] = 'success'
    return json.dumps(response)


def update_user_role_group():
    response = {'response': 'error'}
    if QueryPg(table='group_contacts_',
               child_name=request.args.get('group_id'),
               data={'id': request.args.get('id'),
                     'role_id': request.args.get('role_id')},
               column='role_id').update():
        response['response'] = 'success'
    return json.dumps(response)
