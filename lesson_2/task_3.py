"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:
a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;
c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными.

"""

import yaml
"""
Необходимо преварительно установить модуль "pip install pyyaml" / "poetry add pyyaml"
"""


def save_load_file(data: dict):
    with open('file.yaml', 'w', encoding='utf-8') as f_save:
        yaml.dump(data, f_save, default_flow_style=False, allow_unicode=True, sort_keys=False)

    with open('file.yaml', 'r', encoding='utf-8') as f_load:
        data_1 = yaml.load(f_load, Loader=yaml.SafeLoader)

    return data_1


if __name__ == '__main__':
    DATA_IN = {'items': ['computer', 'printer', 'keyboard', 'mouse'],
           'items_quantity': 4,
           'items_ptice': {'computer': '200€-1000€',
                           'printer': '100€-300€',
                           'keyboard': '5€-50€',
                           'mouse': '4€-7€'}
           }

    DATA_OUT = save_load_file(DATA_IN)
    assert DATA_IN == DATA_OUT
