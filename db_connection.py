import pymysql
import time
from os import getenv


def get_db_connection():
    # Параметры подключения к базе данных
    db_connection = {
        'host': getenv('DATABASE_HOST_ADDRESS'),
        'user': getenv('USERNAME'),
        'password': getenv('DATABASE_PASS'),
        'database': getenv('DATABASE_NAME'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    # Проверка подключения к базе данных
    try:
        connection = pymysql.connect(**db_connection)
        print("Подключение к базе данных установлено")
        return connection
    except pymysql.err.OperationalError as e:
        print("Подключение к базе данных прервано:", str(e))
        print("Пытаюсь восстановить подключение...")
        connection = reconnect(db_connection)
        return connection


def reconnect(db_connection):
    while True:
        # Пытаемся установить подключение каждые 5 секунд
        try:
            connection = pymysql.connect(**db_connection)
            print("Подключение восстановлено")
            return connection
        except pymysql.err.OperationalError as e:
            print("Ошибка восстановления подключения:", str(e))
            time.sleep(5)

