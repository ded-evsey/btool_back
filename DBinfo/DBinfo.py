mongo = {'port': 27017,
         'server': 'localhost',
         'db_name': 'btool'}

posgresql = {'db_name': 'btool',
             'user': 'btool_admin',
             'host': '127.0.0.1',
             'port': '5433',
             'password': 'btool_admin_role'}

pg_tables = {'users': {'id': 'id',
                       'first_name': 'first_name',
                       'second_name': 'second_name',
                       'email': 'email',
                       'tel_number': 'tel_number',
                       'password': 'password',
                       'contacts_list': 'contacts_list',
                       'date_born': 'date_list',
                       'role_sys_id': 'role_sys_id',
                       'role_company_id': 'role_company_id',
                       'tasks_board': 'tasks_board'
                       },
             'user_contacts': {'user_id': 'user_id',
                               'message_box': 'message_box',
                               'friend_id': 'friend_id'
                               },
             'role': {'id': 'id',
                      'name': 'name',
                      'description': 'description',
                      'cost': 'cost',
                      'type': 'type'
                      },
             'groups': {'id': 'id',
                        'name': 'name',
                        'group_contacts': 'group_contacts',
                        'group_message_box': 'group_message_box'
                        },
             'group_contacts': {'group_id': 'group_id',
                                'user_id': 'user_id',
                                'role_id': 'role_id'
                                }

             }

mongo_collections = {'message_box': {'_id': '_id',
                                     'from_id': 'from_id',
                                     'to_id': 'to_id',
                                     'datetime': 'datetime',
                                     'content_message': [{
                                         'type': 'type',
                                         'content': 'content'}]
                                     },
                     'task_board': {'_id': '_id',
                                    'date_appearance': 'date_appearance',
                                    'date_execution': 'date_execution',
                                    'completed': 'completed',
                                    'content_task': [{
                                        'type': 'type',
                                        'content': 'content'}]}
                     }
