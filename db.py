import sqlite3
import json

conn = sqlite3.connect("photo-tagger.db")
##conn = sqlite3.connect(:memory:) # сохранение в RAM
cursor = conn.cursor()

# Создание таблицы
def create_table(cursor):
    cursor.execute("""
    CREATE TABLE pictures
    (pic_id INTEGER PRIMARY KEY, tags json, pic_link TEXT)
    """)

#Удаление таблицы
def delete_table(cursor):
    cursor.execute("""
    DROP TABLE pictures
    """)

##test = json.dumps({'car':'f', 'cat':'t'})

## Добавление данных в БД
def insert_data(conn, cursor, pic_id, pic_tags, pic_link):
    cursor.execute("""
    INSERT INTO pictures
    VALUES (""" + pic_id + """, '[""" + pic_tags + """]', '""" + pic_link + \
    """')""")
    conn.commit()

# Добавление множества данных в БД одновременно через метод "?"
def many_insert_data(conn, cursor, id_list, tag_list, link_list):
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
    cursor.execute("SELECT * FROM pictures")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Вывод содержимого, которое соотвествует заданному параметру
def select_by_param():
    pass

# Обновление БД
def update_table():
    pass
##upd_sql = """
##UPDATE pictures
##SET  = ''
##WHERE = ''
##"""
##cursor.execute(upd_sql)

# Удаление из БД
def delete_table():
    pass
##del_sql = "DELETE FROM pictures WHERE = ''"
##cursor.execute(del_sql)

conn.close()
