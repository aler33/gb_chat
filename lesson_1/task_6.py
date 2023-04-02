"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

import locale
from chardet.universaldetector import UniversalDetector

def_coding = locale.getpreferredencoding()
print(f'Кодировка в системе по-умолчанию: {def_coding}')

with open('test_file.txt', 'w') as f:
    f.write('сетевое программирование\n')
    f.write('сокет\n')
    f.write('декоратор\n')

detector = UniversalDetector()
with open('test_file.txt', 'rb') as f:
    for line in f:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(f'Кодировка файла: {detector.result}')

try:
    with open('test_file.txt', 'r', encoding='utf-8') as f:
        print('Содержимое файла:')
        for line in f:
            print(line.replace('\n', ''))
except UnicodeDecodeError:
    print('Файл записан не в кодировке utf-8')
