from flask import request
from QyeryClass.PostgreSQL import QueryPg
from QyeryClass.Mongodb import QueryMongo
from DBinfo.DBinfo import pg_tables, mongo_collections
import datetime
import json
from bson.objectid import ObjectId


def create_user():
    response = {'response': 'error'}
    data = {}
    cr_dict = pg_tables['users']
    if cr_dict.get('id') != None :
        cr_dict.pop('id')
    if cr_dict.get('contacts_list') != None:
        cr_dict.pop('contacts_list')
    if cr_dict.get('tasks_board') != None:
        cr_dict.pop('tasks_board')
    for key in cr_dict:
        if key == 'role_sys_id' or key == 'role_company_id':
            data[key] = int(request.json.get(key))
        elif key == "date_born":
            data[key] = datetime.datetime.strptime(request.json.get(key), "%Y-%m-%d")
        else:
            data[key] = request.json.get(key)
    user_id = QueryPg(data=data).insert()
    task_board = QueryMongo(collection_type="task_board_u" + user_id, data={mongo_collections['task_board']}).insert()
    if task_board:
        print(task_board)
        QueryMongo(collection_type="task_board_u", name_collection=user_id, data={'_id': ObjectId(task_board)}).delete()
        response['response'] = 'succsess'
    return json.dumps(response)


def delete_user():
    response = {'response': 'error'}
    user = QueryPg(data={'id': request.json.get('id')}).delete()
    if user > 0:
        QueryMongo(collection_type='task_board_u', name_collection=request.json.get('id'), query_type=0).delete()
        response['response'] = 'success'
    return json.dumps(response)


def edit_data_user():
    response = {'response': 'error'}
    user = QueryPg(column=request.json.get('column'), data={'id': request.json.get('id'),
                                                            'new': request.json.get('new')}).update()
    if user:
        response['response'] = 'success'
    return json.dumps(response)


def login():
    response = {'response': 'error'}
    user_email = QueryPg(data={'email': request.json.get('username')}, condition='=').select()
    user_tel = QueryPg(data={'tel_number': request.json.get('username')}, condition='=').select()
    if len(user_email) > 0:
        check_list = user_email
    elif len(user_tel) > 0:
        check_list = user_tel
    else:
        check_list = []
    if len(check_list) > 0:
        for item in check_list:
            if (item['email'] == request.json.get('username') or item['tel_number'] == request.json.get('username')) and item['password'] == request.json.get('password'):
                response['response'] = 'user find, her id = ' + str(item['id'])
                contacts = QueryPg(table=item['contacts_list']).select()
                response['contacts'] = contacts_user(contacts)
            else:
                response['response'] = 'false password'
    return json.dumps(response)


def contacts_user(query_class):
    message_box = {}
    contact_list = {}
    for item in query_class.select():
        message_box['contact'] = item['friend_id']
        message_box[item['message_box']] = QueryMongo(collection_type=item['message_box'], query_type=0)
        message_box[item['message_box']].select()
        contact_list[item['message_box']] = {message_box}
        message_box.clear()
    return message_box


def new_contact_user():
    response = {'response': 'error'}
    initiator_id = request.json.get('user_id')
    invite_id = request.json.get('friend_id')
    name_box = 'message_box_u'+initiator_id+"_u"+invite_id
    if len(QueryPg(table='user_contacts', data={'message_box': name_box}).select()) == 0:
        id_message = QueryMongo(collection_type=name_box, data={mongo_collections['message_box']}).insert()
        QueryMongo(collection_type=name_box, data={"_id": ObjectId(id_message)}).delete()
        QueryPg(table='user_contacts_'+initiator_id, data={'user_id': initiator_id,
                                                           'friend_id': invite_id, 'message_box': name_box}).insert()
        QueryPg(table='user_contacts_'+invite_id, data={'user_id': invite_id,
                                                        'friend_id': initiator_id, 'message_box': name_box}).insert()
        response['response'] = 'success'
    return json.dumps(response)


def delete_contact_user():
    response = {'response': 'error'}
    initiator_id = request.json.get('user_id')
    invite_id = request.json.get('friend_id')
    name_box = QueryPg(table='user_contacts', child_name='_' + initiator_id, data={'friend_id': invite_id}).select()
    for item in name_box:
        if QueryPg(table='user_contacts', data={'message_box': item['message_box']}).delete() == 2:
            QueryMongo(collection_type=str(item['message_box']), query_type=0).delete()
            response['response'] = 'success'
    return json.dumps(response)


def add_role():
    response = {'response': 'error'}
    if QueryPg(table='role',
               data={'name': request.json.get('name'),
                     'discription': request.json.get('discription'),
                     'cost': request.json.get('cost')}).insert():
        response['response'] = 'success'
    return json.dumps(response)
