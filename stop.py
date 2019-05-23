import os

if __name__ == "__main__":
    os.system("c:/Users/evsee/PycharmProjects/btool_back/pg/bin/pg_ctl.exe stop -D"
              " C:/Users/evsee/PycharmProjects/btool_back/pg/data -m smart")
    os.system('taskkill /F /IM mongod.exe /T')
