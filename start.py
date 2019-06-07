import os


def start(command_string):
    return os.system(command_string)


if __name__ == '__main__':
    pg_string = '"C:/ProgramFiles/PostgreSQL/11/bin/pg_ctl.exe" start ' \
                '-D D:/PycharmProject/btool_back/pg/data'
    mongo_string = '"C:/ProgramFiles/MongoDB/Server/4.0/bin/mongod.exe" ' \
                   '--dbpath D:/PycharmProject/btool_back/mongoDB/data'
    start(pg_string)
    start(mongo_string)
