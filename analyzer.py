import os
import uuid
from imageai.Detection import ObjectDetection
from pathlib import Path

#обработка фотки
def photos(title):
    list = detector.detectObjectsFromImage(
            input_image=os.path.join(exec_path, title),
            output_image_path=os.path.join(exec_path, "./test/new_objects.jpg"),
            minimum_percentage_probability=50
    )
    tags = '{'
    for eachObject in list:
            if eachObject["name"] not in tags: 
                tags += '"name":"' + eachObject["name"] + '",'
    tags = tags[:-1]
    tags += '}'
    #print(tags, "\n", title)

#поиск фоток
def enumerate_files(dir_path: Path, ext: str):
    # формируем маску для поиска
    path_mask = '*.%s' % ext
    # исключаем директории
    only_files = [
        f for f in dir_path.glob(path_mask)
        if f.is_file()
    ]
    for f_path in only_files:
        photos(f_path)

#создание модели
exec_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(exec_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

parent_dir = Path(exec_path)
enumerate_files(parent_dir, 'jpg')
