import os

def start(command_stryng):
    os.system(command_stryng)
    return 1


if __name__ == '__main__':
    pg_string = "c:/Users/evsee/PycharmProjects/btool_back/pg/bin/pg_ctl.exe start -D C:/Users/evsee/" \
               "PycharmProjects/btool_back/pg/data"
    mongo_string = "c:/Users/evsee/PycharmProjects/btool_back/mongoDB/bin/mongod.exe --dbpath C:/Users/evsee/" \
                   "PycharmProjects/btool_back/mongoDB/data"
    start(pg_string)
    start(mongo_string)
