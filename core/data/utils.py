import json
import mysql.connector
from os import getenv


def load_json_data():
    with open('quotes_data.json', 'r') as f:
        quotes1 = json.load(f)

    with open('quotes_luke_data.json', 'r') as f:
        quotes2 = json.load(f)

    with open('quotes_obi_data.json', 'r') as f:
        quotes3 = json.load(f)

    with open('quotes_vader_data.json', 'r') as f:
        quotes4 = json.load(f)

    quotes_data = [quotes1 + quotes2 + quotes3 + quotes4][0]
    return quotes_data


def insert_data_to_db(data):
    # Установить параметры подключения
    config = {
      'user': getenv('USERNAME') or 'username',
      'password': getenv('DATABASE_PASS') or 'password',
      'host': getenv('DATABASE_HOST_ADDRESS') or 'localhost',
      'database': getenv('DATABASE_NAME') or 'AMITDB',
      'raise_on_warnings': True
    }

    # Создать подключение
    cnx = mysql.connector.connect(**config)

    # Создать объект-курсор для выполнения запросов
    cursor = cnx.cursor()

    for quote in data:
        # Выполнить SQL запрос
        query = f"""INSERT quotes_static(quote, quote_translation) VALUES ('{quote["quote"]}', '{quote["quote_translation"]}');"""
        cursor.execute(query)
        cnx.commit()

    # Закрыть подключение
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    insert_data_to_db(load_json_data())
    print('data loaded!')
