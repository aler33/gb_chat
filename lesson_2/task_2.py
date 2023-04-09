"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:
a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
(item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
должна предусматривать запись данных в виде словаря в файл orders.json. При
записи данных указать величину отступа в 4 пробельных символа;
b. Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра.

"""

import json


def write_order_to_json(item: str, quantity: str, price: str, buyer: str, date: str):
    try:
        with open('orders.json', 'r', encoding='utf-8') as f_load:
            data = json.load(f_load)
    except Exception:
        data = {'orders': []}

    with open('orders.json', 'w', encoding='utf-8') as f_save:
        orders = data['orders']
        new_order = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
        }
        orders.append(new_order)
        json.dump(data, f_save, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    write_order_to_json('printer', '10', '16700', 'Ivanov I.I.', '12.04.2023')
    write_order_to_json('scaner', '20', '12000', 'Petrov P.P.', '11.12.2022')
    write_order_to_json('computer', '5', '70000', 'Sidorov S.S.', '2.03.2023')
