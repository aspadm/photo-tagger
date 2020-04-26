"""
@author: Шибанова Д.А., ИУ7-82Б

Файл работы с базой данных.

Техническое задание:
Разработать десктоп-приложение для подбора снимков по тегам.
Предусмотреть перечень тегов, которые могут быть установлены
пользователем вручную. Пользователь может:
загрузить снимки в систему;
указать теги из числа предложенных вручную;
установить автоопределение тегов на основе анализа снимка;
производить поиск по тегу из перечня фильтров.
"""

import sqlite3
import json

conn = sqlite3.connect("photo-tagger.db")
##conn = sqlite3.connect(:memory:) # сохранение в RAM
cursor = conn.cursor()

# Создание таблицы
def create_table(cursor):
    """
    Создаёт таблицу в базе данных sqlite3 с тремя столбцами.

    :param cursor: курсор
    :type pic_id: integer primary key
    :type tags: json
    :type pic_link: text
    :rtype: None
    
    """
    
    cursor.execute("""
    CREATE TABLE pictures
    (pic_id INTEGER PRIMARY KEY, tags json, pic_link TEXT)
    """)

#Удаление таблицы
def delete_table(cursor):
    """
    Удаляет таблицу со снимками.

    :param cursor: курсор
    :rtype: None
    
    """
    
    cursor.execute("""
    DROP TABLE pictures
    """)

##test = json.dumps({'car':'f', 'cat':'t'})

## Добавление данных в БД
def insert_data(conn, cursor, pic_id, pic_tags, pic_link):
    """
    Добавляет одну строку данных в БД.

    :param conn: соединение
    :param cursor: курсор
    :param pic_id: идентификатор снимка
    :param pic_tags: теги изображения
    :param pic_link: адрес изображения
    :type pic_id: integer primaty key (int)
    :type pic_tags: json
    :type pic_link: text (str)
    :rtype: None
    
    """
    
    cursor.execute("""
    INSERT INTO pictures
    VALUES (""" + pic_id + """, '[""" + pic_tags + """]', '""" + pic_link + \
    """')""")
    conn.commit()

# Добавление множества данных в БД одновременно через метод "?"
def many_insert_data(conn, cursor, id_list, tag_list, link_list):
    """
    Добавляет одновременно более одной строки данных в БД через метод "?"

    :param conn: соединение
    :param cursor: курсор
    :param id_list: список идентификаторов
    :param tag_list: список тегов
    :param link_list: список ссылок на снимок
    :type id_list: массив integer'ов
    :type tag_list: массив json
    :type link_list: массив строк
    :rtype: None
    
    """
    
    len_id = len(id_list)
    if len_id == len(tag_list) and len_id == len(link_list):
        for i in range(len_id-1):
            pass
##        cursor.executemany("INSERT INTO pictures VALUES (?, ?, ?)", pictures)
##        conn.commit()
        ##pictures = [('1', '{car:}', ''),
        ##            ('2', '', ''),
        ##            ('3', '', ''),
        ##            ('4', '', '')]
        ##cursor.executemany("INSERT INTO pictures VALUES (?, ?, ?)", pictures)

# Вывод всего содержимого БД
def select_all(cursor):
    """
    Выводит все строки БД.

    :param cursor: курсор
    :rtype: None
    """
    
    cursor.execute("SELECT * FROM pictures")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Вывод содержимого, которое соотвествует заданному параметру
def select_by_param():
    """
    Выводит все строки, соответствующие заданному параметру.

    
    """
    
    pass

# Обновление БД
def update_table():
    """
    Обновляет БД.
    
    """
    
    pass
##upd_sql = """
##UPDATE pictures
##SET  = ''
##WHERE = ''
##"""
##cursor.execute(upd_sql)

# Удаление из БД
def delete_from_table():
    """
    Удаляет заданную строку из БД.
    """
    
    pass
##del_sql = "DELETE FROM pictures WHERE = ''"
##cursor.execute(del_sql)

conn.close()

if __name__ == "__main__":
    pass
