import json
from flask import Flask
from ModuleBtool import message, task, user, group

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_class():
    response = {'response': 'Pleas enter correct URL'}
    return json.dumps(response)


@app.route('/create_user', methods=['POST'])
def create_user():
    return user.create_user()


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    return user.delete_user()


@app.route('/edit_user_data', methods=['PUT'])
def edit_data_user():
    return user.edit_data_user()


@app.route('/login', methods=['GET'])
def login():
    return user.login()


@app.route('/new_contact_user', methods=["POST"])
def new_contact_user():
    return user.new_contact_user()


@app.route('/delete_contact_user', methods=['DELETE'])
def delete_contact_user():
    return user.delete_contact_user()


@app.route('/send_message', methods=['POST'])
def send_message():
    return message.send_message()


@app.route('/rewrite_message', methods=['PUT'])
def rewrite_message():
    return message.rewrite_message()


@app.route('/delete_message', methods=['DELETE'])
def delete_message():
    return message.delete_message()


@app.route('/show_message', methods=['GET'])
def show_message():
    return message.show_message()


@app.route('/new_group', methods=['POST'])
def new_group():
    return group.new_group()


@app.route('/delete_group', methods=['DELETE'])
def delete_group():
    return group.delete_group()


@app.route('/update_group', methods=['PUT'])
def update_group():
    return group.update_group()


@app.route('/new_user_group', methods=['POST'])
def new_user_group():
    return group.new_user_group()


@app.route('/delete_user_group', methods=['DELETE'])
def delete_user_group():
    return group.delete_user_group()


@app.route('/update_user_role_group', methods=['PUT'])
def update_user_role_group():
    return group.update_user_role_group()


@app.route('/create_task/<type>', methods=['POST'])
def create_task(type):
    return task.create_task(type)


@app.route('/complete_task', methods=['PUT'])
def complete_task():
    return task.complete_task()


@app.route('/edit_task', methods=['PUT'])
def edit_task():
    return task.edit_task()


@app.route('/delete_task', methods=['DELETE'])
def delete_task():
    return task.delete_task()


@app.route('/check_success_task', methods=['GET'])
def check_success_task():
    return task.check_success_task()


if __name__ == '__main__':
    app.run()
