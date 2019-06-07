import psycopg2
from psycopg2 import sql
from DBinfo import pg_tables, posgresql
conn = psycopg2.connect(dbname=posgresql['db_name'], user=posgresql['user'],
                        host=posgresql['host'], port=posgresql['port'], password=posgresql['password'])
conn.autocommit = True
cursor = conn.cursor()


def start(pg=cursor):
    """
    Функция получения курсора для дальнейшей работы в других файлах
    :param pg: курсор(опционально)
    :return: курсор
    """
    return pg


def finish(pg=cursor):
    """
    Функция завершения работы с базой данных
    :param pg: курсор
    :return: 0
    """
    pg.close()
    conn.close()
    return 0


class QueryPg(object):
    """
    Класс, для запросов к базе PostgreSQL
        :param table: таблица, к которой происходит запрос
        :param column: какие столбцы запрашивать
        :param data: условия выборки
        :param condition: оператор сравнения
        :param pg: курсор
    """
    def __init__(self, table='users', child_name='', column='*', data={}, condition='=', pg=cursor):
        self.table = table
        self.child_table = table + child_name
        self.column = column
        self.data = data
        self.condition = condition
        self.pg = pg

    def select(self):
        """
        Составление запроса на вывод информации
        :return: выборка
        """
        response = []
        if self.data != {} and self.column != '*':
            key, value = self.data.popitem()
            que = "SELECT {} FROM {} WHERE {}" + self.condition + "%s;"
            select_str = sql.SQL(que).format(sql.SQL(',').join(map(sql.Identifier, self.column)),
                                             sql.Identifier(self.child_table), sql.Identifier(key), value)
        elif self.data != {} and self.column == "*":
            key, value = self.data.popitem()
            que = "SELECT * FROM {} WHERE {}" + self.condition + "{};"
            select_str = sql.SQL(que).format(sql.Identifier(self.child_table), sql.Identifier(key), sql.Literal(value))
        elif self.data == {} and self.column != '*':
            que = "SELECT {} FROM {};"
            select_str = sql.SQL(que).format(sql.SQL(',').join(map(sql.Identifier, self.column)),
                                             sql.Identifier(self.child_table))
        else:
            que = "SELECT * FROM {};"
            select_str = sql.SQL(que).format(sql.Identifier(self.child_table))
        query_str = select_str.as_string(self.pg)
        self.pg.execute(query_str)
        for val in self.pg.fetchall():
            response.append(dict(zip(pg_tables[self.table].values(), val)))
        return response

    def insert(self):
        """
        Составление запроса на добавления информации в таблицу
        :return: результат запроса
        """
        que = "INSERT INTO {}({}) VALUES ({}) RETURNING ID;"
        insert_str = sql.SQL(que).format(sql.Identifier(self.table),
                                         sql.SQL(',').join(map(sql.Identifier, self.data.keys())),
                                         sql.SQL(',').join(map(sql.Literal, self.data.values()))).as_string(self.pg)
        self.pg.execute(insert_str)
        for val in self.pg.fetchone():
            return str(val)

    def delete(self):
        """
        Составление запроса для удаления записи из таблицы
        :return: результат запроса
        """
        que = "delete from {} WHERE {} = {};"
        col, value = self.data.popitem()
        delete_str = sql.SQL(que).format(sql.Identifier(self.table), sql.Identifier(col), sql.Literal(value))\
            .as_string(self.pg)
        self.pg.execute(delete_str)
        return self.pg.rowcount

    def update(self):
        """
        Составление запроса для изменения записи в таблице
        :return: результат запроса
        """
        id, new = self.data.values()
        que = 'UPDATE {} set {} = {} where "id"' + self.condition + '{};'
        update_str = sql.SQL(que).format(sql.Identifier(self.table), sql.Identifier(self.column),
                                         sql.Literal(new), sql.Literal(id)).as_string(self.pg)
        self.pg.execute(update_str)
        return self.pg.rowcount


if __name__ == '__main__':
    start()
