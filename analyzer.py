"""
@author: Алексеевский Р.А., ИУ7-84Б

Файл работы с определением содержимого снимка.

Техническое задание:
Разработать десктоп-приложение для подбора снимков по тегам.
Предусмотреть перечень тегов, которые могут быть установлены
пользователем вручную. Пользователь может:
загрузить снимки в систему;
указать теги из числа предложенных вручную;
установить автоопределение тегов на основе анализа снимка;
производить поиск по тегу из перечня фильтров.
"""

import os
import os.path
from imageai.Detection import ObjectDetection

class TagsDetector:
    """
    Определитель тегов по файлу изображения.

    :param model: путь до модели нейросети
    :type model: str
    """
    def __init__(self, model=None):
        if model is None:
            exec_path = os.getcwd()
            model = os.path.join(exec_path, "resnet50_coco_best_v2.0.1.h5")

        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(model)
        self.detector.loadModel()

    def getImageTags(self, filepath: str) -> list:
        """
        Обрабатывает фотографию, определяет её содержимое.

        :param filepath: путь к файлу
        :type filepath: str
        :rtype: list
        """

        _, raw = self.detector.detectObjectsFromImage(
                input_image=filepath,
                output_type="array",
                minimum_percentage_probability=50)

        tags = []
        for tag in raw:
            if tag["name"] not in tags: 
                tags.append(tag["name"])

        return sorted(tags)

    def getNewFiles(self, dir_path: str, excluded: list, ext: list) -> dict:
        """
        Производит поиск фотографий внутри директории и присваивает им теги.

        :param dir_path: путь до директории, в которой хранятся снимки
        :param excluded: имена файлов, которые не нужно обрабатывать
        :param ext: расширения изображений для обработки
        :type dir_path: str
        :type excluded: list
        :type ext: list
        :rtype: dict
        """

        res = {}

        for fname in os.listdir(dir_path):
            fpath = os.path.join(dir_path, fname)
            if os.path.isfile(fpath) and \
               os.path.splitext(fpath)[-1].lower() in ext and \
               fpath not in excluded:
                res.update({fpath: self.getImageTags(fpath)})

        return res

if __name__ == "__main__":
    detector = TagsDetector()
    print(detector.getImageTags("test.jpg"))
    print(detector.getImageTags("test2.jpg"))
    print(detector.getNewFiles(".", [], [".jpg", ".png"]))
