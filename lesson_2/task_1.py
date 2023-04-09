"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);
b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;
c. Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import os
import re


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    file_txt_list = [f for f in file_list if f.split('.')[-1] == 'txt']
    file_txt_list.sort()

    for fil in file_txt_list:
        with open(fil, 'r', encoding='cp1251') as f_load:
            data = f_load.read()
            prod_pattern = re.compile(r'Изготовитель системы:\s*\S*')
            os_prod_list.append(prod_pattern.findall(data)[0].split()[-1])

            name_pattern = re.compile(r'Название ОС:.*')
            os_name_list.append(' '.join(name_pattern.findall(data)[0].split()[2:5]))

            code_pattern = re.compile(r'Код продукта:\s*\S*')
            os_code_list.append(code_pattern.findall(data)[0].split()[-1])

            type_pattern = re.compile(r'Тип системы:\s*\S*')
            os_type_list.append(type_pattern.findall(data)[0].split()[-1])

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    j = 1

    for i in range(0, 3):
        row_data = []
        row_data.append(j)
        row_data.append(os_prod_list[i])
        row_data.append(os_name_list[i])
        row_data.append(os_code_list[i])
        row_data.append(os_type_list[i])
        main_data.append(row_data)
        j += 1
    return main_data


def write_to_csv(out_file: str):

    main_data = get_data()
    with open(out_file, 'w', encoding='utf-8') as f_save:
        writer = csv.writer(f_save, quoting=csv.QUOTE_NONNUMERIC)
        for row in main_data:
            writer.writerow(row)


if __name__ == '__main__':
    write_to_csv('data_report.csv')
