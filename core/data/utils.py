import json
from os import getenv
from db_connection import get_db_connection

INSERT_QUERY = 'INSERT {table_name}{field_list} VALUES {values_list};'


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
    cursor = get_db_connection().cursor()
    cursor.execute('SHOW TABLES;')
    bases = cursor.fetchall()
    print(bases)
    print('quotes_star_wars' in bases)
    print('quotes_star_war1s' in bases)


def insert_data_to_db(data, table_name):
    cursor = get_db_connection().cursor()

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
            cnx.commit()
        except:
            print('ERROR' + str(query))

    # Закрыть подключение
    cursor.close()
    cnx.close()

