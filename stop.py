import os

if __name__ == "__main__":
    os.system('"C:/ProgramFiles/PostgreSQL/11/bin/pg_ctl.exe" stop -D'
              " D:/PycharmProject/btool_back/pg/data -m smart")
    os.system('taskkill /F /IM mongod.exe /T')
