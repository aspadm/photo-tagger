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

class LocalBase:
    """
    Работа с локальной БД SQLite3.
    """
    def __init__(self, path=None):
        if path is None:
            path = "photo-tagger.db"

        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT count(name) FROM sqlite_master
            WHERE type='table' AND name='pictures'""")

        if self.cursor.fetchone()[0] != 1:
            self.createTable()

    def __del__(self):
        self.conn.close()

    def createTable(self) -> None:
        """
        Создаёт таблицу в базе данных sqlite3 с двумя столбцами.

        :type pic_id: text primary key
        :type tags: json
        """
        self.cursor.execute("""CREATE TABLE pictures
            (pic_id TEXT PRIMARY KEY, tags json)""")

    def deleteTable(self) -> None:
        """
        Удаляет таблицу со снимками.
        """
        self.cursor.execute("DROP TABLE pictures")

    def getFilenames(self) -> list:
        """
        Возвращает все имеющиеся в базе имена файлов.

        :rtype: list
        """
        self.cursor.execute("SELECT pic_id FROM pictures")
        rows = self.cursor.fetchall()

        return [row[0] for row in rows]

    def addImage(self, pic_id: str, pic_tags: list) -> None:
        """
        Добавляет одно изображение в БД.

        :param pic_id: идентификатор снимка
        :param pic_tags: теги изображения
        :type pic_id: str
        :type pic_tags: list
        """
        self.cursor.execute("""INSERT INTO pictures
            VALUES ('{}', '{}')""".format(pic_id, json.dumps(pic_tags)))
        self.conn.commit()

    def addImages(self, images: dict) -> None:
        """
        Добавляет несколько изображений в БД.

        :param images: пары изображение:теги
        :type images: dict
        """
        for image_name, image_tags in images.items():
            self.addImage(image_name, image_tags)

    def getImages(self) -> dict:
        """
        Возвращает все изображения из БД.

        :rtype: dict
        """
        self.cursor.execute("SELECT * FROM pictures")
        rows = self.cursor.fetchall()

        return {row[0]:json.loads(row[1]) for row in rows}

    def getImage(self, pic_id: str) -> list:
        """
        Возвращает теги изображения из БД.

        :param pic_id: идентификатор снимка
        :type pic_id: str
        :rtype: list
        """
        self.cursor.execute("""SELECT tags FROM pictures
            WHERE pic_id = '{}'""".format(pic_id))
        rows = self.cursor.fetchall()

        return json.loads(rows[0][0]) if len(rows) else None

    def getFilenamesByTags(self, tags: list) -> list:
        """
        Выводит все изображения, соответствующие заданным тегам.

        :param tags: список тегов
        :type tags: list
        """
        res = []

        images = self.getImages()
        for image_name, image_tags in images.items():
            for img_tag in image_tags:
                if img_tag in tags:
                    res.append(image_name)
                    continue

        return res

    def updateImage(self, pic_id: str, pic_tags: list) -> None:
        """
        Обновляет одно изображение в БД.

        :param pic_id: идентификатор снимка
        :param pic_tags: теги изображения
        :type pic_id: str
        :type pic_tags: json
        """
        self.cursor.execute("""UPDATE pictures SET tags = '{}'
            WHERE pic_id = '{}'""".format(json.dumps(pic_tags), pic_id))
        self.conn.commit()

    def deleteImage(self, pic_id: str) -> None:
        """
        Удаляет заданное изображение из БД.

        :param pic_id: идентификатор снимка
        :type pic_id: str
        """
        self.cursor.execute("""DELETE FROM pictures
            WHERE pic_id = '{}'""".format(pic_id))
        self.conn.commit()

if __name__ == "__main__":
    base = LocalBase()
    base.addImage("test", ["cat", "trolley"])
    base.addImage("test2", ["human"])
    print(base.getFilenames())
    print(base.getImages())
    print(base.getImage("test"))
    print(base.getImage("test0"))
    print(base.getFilenamesByTags(["cat", "horse"]))
    base.updateImage("test2", ["horse", "pig"])
    print(base.getImages())
    base.deleteImage("test2")
    print(base.getFilenames())
    base.deleteTable()
