from PostgreSQL import QueryPg
from Mongodb import QueryMongo
import datetime
import DBinfo as db
import json
import pymongo as mongo
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_class():
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


@app.route('/create_user', methods=['POST'])
def create_user():
    response = {'response': 'error'}
    data = {}
    cr_dict = db.pg_tables['users']
    if cr_dict.get('id') != None :
        cr_dict.pop('id')
    if cr_dict.get('contacts_list') != None:
        cr_dict.pop('contacts_list')
    if cr_dict.get('tasks_board') != None:
        cr_dict.pop('tasks_board')
    for key in cr_dict:
        if key == 'role_sys_id' or key == 'role_company_id':
            data[key] = int(request.args.get(key))
        elif key == "date_born":
            data[key] = datetime.datetime.strptime(request.args.get(key), "%Y-%m-%d")
        else:
            data[key] = request.args.get(key)
    user = QueryPg(data=data)
    user_id = user.insert()
    task_board = QueryMongo(collection_type="task_board_u" + user_id, data={})
    task_board.insert()
    response['response'] = 'succsess'
    return json.dumps(response)


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    response = {'response': 'user not found'}
    user = QueryPg(data={'id': request.args.get('id')}).delete()
    if user > 0:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/edit_user_data', methods=['PUT'])
def edit_data_user():
    response = {'response': 'user not found'}
    user = QueryPg(column=request.args.get('column'), data={'id': request.args.get('id'),
                                                            'new': request.args.get('new')}).update()
    if user:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/login', methods=['GET'])
def login():
    response = {'response': 'user not found'}
    user_email = QueryPg(data={'email': request.args.get('username')}, condition='=').select()
    user_tel = QueryPg(data={'tel_number': request.args.get('username')}, condition='=').select()
    if len(user_email) > 0:
        check_list = user_email
    elif len(user_tel) > 0:
        check_list = user_tel
    else:
        check_list = []
    if len(check_list) > 0:
        for item in check_list:
            if (item['email'] == request.args.get('username') or item['tel_number'] == request.args.get('username')) and item['password'] == request.args.get('password'):
                response['response'] = 'user find, her id = ' + str(item['id'])
                contacts = QueryPg(table=item['contacts_list'])
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


@app.route('/new_contact_user', methods=["POST"])
def new_contact_user():
    response = {'response': 'error'}
    initiator_id = request.args.get('user_id')
    invite_id = request.args.get('friend_id')
    name_box = 'message_box_u'+initiator_id+"_u"+invite_id
    if len(QueryPg(table='user_contacts', data={'message_box': name_box}).select()) == 0:
        QueryMongo(collection_type=name_box, data={}).insert()
        QueryPg(table='user_contacts_'+initiator_id, data={'user_id': initiator_id,
                                                           'friend_id': invite_id, 'message_box': name_box}).insert()
        QueryPg(table='user_contacts_'+invite_id, data={'user_id': invite_id,
                                                        'friend_id': initiator_id, 'message_box': name_box}).insert()
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/delete_contact_user', methods=['DELETE'])
def delete_contact_user():
    response = {'response': 'error'}
    initiator_id = request.args.get('user_id')
    invite_id = request.args.get('friend_id')
    name_box = QueryPg(table='user_contacts', child_name='_' + initiator_id, data={'friend_id': invite_id}).select()
    for item in name_box:
        if QueryPg(table='user_contacts', data={'message_box': item['message_box']}).delete() == 2:
            QueryMongo(collection_type=str(item['message_box']),query_type=0).delete()
            response['response'] = 'success'
    return json.dumps(response)


@app.route('/send_message', methods=['POST'])
def send_message():
    # TODO: need test
    response = {'response': 'error'}
    message = QueryMongo(name_collection=request.args.get('table_name'),
                         data={'from_id': request.args.get('from_id'),
                               'to_id': request.args.get('to_id'),
                               'content_message': [
                                   {'type': request.args.get('type'),
                                    'content': request.args.get('content')}]}).insert()
    if message:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/rewrite_message', methods=['PUT'])
def rewrite_message():
    # TODO: need test
    response = {'response': 'error'}
    message = QueryMongo(name_collection=request.args.get('table_name'),
                         data={'_id': request.args.get('id')},
                         update_data={'$set': {'message_content': [
                                                   {'content': request.args.get('new_content')}]}}).update()
    if message:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/delete_message', methods=['DELETE'])
def delete_message():
    # TODO: need test
    response = {'response': 'error'}
    message = QueryMongo(collection_type=request.args.get('table_name'), data={'_id': request.args.get('id')})
    if message:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/show_message', methods=['GET'])
def show_message():
    # TODO: need test, unfully
    response = {'response': 'error'}
    message = QueryMongo(collection_type=request.args.get('table_name'), query_params={'datetime': 1}, query_type=0)
    if message:
        response['response'] = 'success'
        response['messages'] = message
    return json.dumps(response)


@app.route('/new_group', methods=['POST'])
def new_group():
    # TODO: need test
    response = {'response': 'error'}
    data = {}
    cr_dict = db.pg_tables['groups']
    if cr_dict.get('id') !=None :
        cr_dict.pop('id')
    if cr_dict.get('group_contact') !=None :
        cr_dict.pop('group_contact')
    if cr_dict.get('group_message_box') !=None :
        cr_dict.pop('group_message_box')
    for key in cr_dict:
        data[key] = request.args.get(key)
    group = QueryPg(table='groups', data=data)
    group_id = group.insert()
    message_box = QueryMongo(collection_type='message_box_g'+group_id, data={}).insert()
    if message_box:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/delete_group', methods=['DELETE'])
def delete_group():
    # TODO: need test
    response = {'response': 'Pleas enter correct URL'}
    group = QueryPg(table='groups', data={'id': request.args.get('id')}).delete()
    if group > 0:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/update_group', methods=['PUT'])
def update_group():
    # TODO: need test
    response = {'response': 'Pleas enter correct URL'}
    group = QueryPg(table='groups',
                    data={'id': request.args.get('id'),
                          'new': request.args.get('new')},
                    column='name').update()
    if group:
        response['response'] = 'success'
    return json.dumps(response)


@app.route('/new_user_group', methods=['POST'])
def new_user_group():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


@app.route('/delete_user_group', methods=['DELETE'])
def delete_user_group():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


#TODO:тут начинается боль
@app.route('/create_task', methods=['POST'])
def create_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)
#TODO:тут заканчивается боль


@app.route('/complete_task', methods=['PUT'])
def complete_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


@app.route('/edit_task', methods=['PUT'])
def edit_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


@app.route('/delete_task', methods=['DELETE'])
def delete_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


@app.route('/check_success_task', methods=['GET'])
def check_success_task():
    # TODO: need test, unfully
    response = {{'response': 'Pleas enter correct URL'}}
    return json.dumps(response)


if __name__ == '__main__':
    app.run()
