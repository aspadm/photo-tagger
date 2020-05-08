import os
import os.path
from imageai.Detection import ObjectDetection

import yaml

def pytest_generate_tests(metafunc):

    # Пропускаем все функции, у которых нет аргумента filepath
    if 'filepath' not in metafunc.fixturenames:
        return

    # Определяем директорию текущего файла
    dir_path = os.path.dirname(os.path.abspath(metafunc.module.__file__))

    # Определяем путь к файлу с данными
    file_path = os.path.join(dir_path, metafunc.function.__name__ + '.yaml')
    # Открываем выбранный файл
    with open(file_path) as f:
        test_cases = yaml.full_load(f)

    # Предусматриваем неправильную загрузку и пустой файл
    if not test_cases:
        raise ValueError("Test cases not loaded")

    return metafunc.parametrize("filepath, result", test_cases)

import pytest
from analyzer import *

#@pytest.mark.parametrize('filepath, result', test_cases)
def test_getImageTags(filepath, result):
    detector = TagsDetector()
##    print(detector.getImageTags(filepath).__repr__())
##    print(result.__repr__())
    assert detector.getImageTags(filepath) == result
