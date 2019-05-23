import pymongo as mongo
import DBinfo
import json_collections

conn = mongo.MongoClient(DBinfo.mongo['server'], DBinfo.mongo['port'])
db = conn[DBinfo.mongo['db_name']]


def get_collection(collection_type, name_collection='', db_name=db):
    if( collection_type == "message_box" or collection_type == "task_board"):
        full_name_collection = collection_type + "_" + name_collection
    else:
        full_name_collection = collection_type
    return db_name[full_name_collection]


def collection_list(data_base=db):
    return data_base.list_collection_names()


class QueryMongo:
    def __init__(self, collection_type='', name_collection='', data=(), update_data={}, query_type=1, query_params={}):
        self.name_collection = get_collection(collection_type, name_collection)
        self.data = data
        self.type = query_type
        self.update_data = update_data
        self.params = query_params

    def insert(self):
        if self.type:
            return self.name_collection.insert_one(self.data).inserted_id
        else:
            return self.name_collection.insert.inserted_id

    def select(self):
        if self.type:
            return self.name_collection.find_one(self.data, self.params)
        else:
            return self.name_collection.find(self.data, self.params)

    def delete(self):
        if self.type:
            return self.name_collection.delete_one(self.data)
        else:
            return self.name_collection.drop()

    def update(self):
        if self.type:
            return self.name_collection.update_one(self.data, self.update_data)
        else:
            return self.name_collection.update_many(self.data, self.update_data)
