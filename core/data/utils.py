import json
import mysql.connector
from os import getenv


def load_json_data():
    with open('quotes.json', 'r') as f:
        quotes1 = json.load(f)

    with open('luke_quotes.json', 'r') as f:
        quotes2 = json.load(f)

    with open('obi_quotes.json', 'r') as f:
        quotes3 = json.load(f)

    with open('vader_quotes.json', 'r') as f:
        quotes4 = json.load(f)

    quotes_data = [quotes1 + quotes2 + quotes3 + quotes4][0]
    return quotes_data


def insert_data_to_db(data):
    # Установить параметры подключения
    config = {
      'user': getenv('USERNAME'),
      'password': getenv('DATABASE_PASS'),
      'host': getenv('DATABASE_HOST_ADDRESS'),
      'database': getenv('DATABASE_NAME'),
      'raise_on_warnings': True
    }

    # Создать подключение
    cnx = mysql.connector.connect(**config)

    # Создать объект-курсор для выполнения запросов
    cursor = cnx.cursor()

    for quote in data:
        # Выполнить SQL запрос
        query = f"""INSERT quotes_star_wars(quote, quote_translation, author_en, author_ru) 
                    VALUES ('{quote["quote"]}', '{quote["quote_translation"]}', '{quote["author_en"]},
                    '{quote["author_ru"]}');"""
        cursor.execute(query)
        cnx.commit()

    # Закрыть подключение
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    insert_data_to_db(load_json_data())
    print('data loaded!')
