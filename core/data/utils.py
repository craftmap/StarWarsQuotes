import json
from db_connection import db_connection

INSERT_QUERY = 'INSERT {table_name}{field_list} VALUES {values_list};'
CREATE_TABLE_QUERY = """CREATE TABLE {table_name}(
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
quote TEXT NOT NULL,
quote_translation TEXT NOT NULL,
author_en TEXT NOT NULL,
author_ru TEXT NOT NULL
);"""


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


def table_exist(table_name):
    with db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SHOW TABLES;')
        docs = cursor.fetchall()
        if not docs:
            return False
        bases = sum([list(doc.values()) for doc in docs], [])
        cursor.close()
        return table_name in bases


def insert_data_to_db(data, table_name):
    with db_connection() as connection:
        cursor = connection.cursor()

        for quote in data:
            # Выполнить SQL запрос
            try:
                # query = f"""INSERT quotes_star_wars(quote, quote_translation, author_en, author_ru) VALUES ('{quote["quote"]}', '{quote["quote_translation"]}', '{quote["author_en"]}', '{quote["author_ru"]}');"""
                query = INSERT_QUERY.format(
                    table_name=table_name,
                    field_list=('quote', 'quote_translation', 'author_en', 'author_ru'),
                    values_list=({quote["quote"]}, {quote["quote_translation"]}, {quote["author_en"]}, {quote["author_ru"]})
                )
                cursor.execute(query)
                connection.commit()
            except:
                print('ERROR' + str(query))

        # Закрыть подключение
        cursor.close()
