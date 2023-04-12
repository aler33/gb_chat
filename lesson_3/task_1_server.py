"""
Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant
messaging):
a. клиент отправляет запрос серверу;
b. сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих
соответствующие функции.
Функции клиента:
● сформировать presence-сообщение;
● отправить сообщение серверу;
● получить ответ сервера;
● разобрать сообщение сервера;
● параметры командной строки скрипта client.py <addr> [<port>]:
○ addr — ip-адрес сервера;
○ port — tcp-порт на сервере, по умолчанию 7777.
Функции сервера:
● принимает сообщение клиента;
● формирует ответ клиенту;
● отправляет ответ клиенту;
● имеет параметры командной строки:
○ -p <port> — TCP-порт для работы (по умолчанию использует 7777);
○ -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все
доступные адреса).
"""

from socket import *
import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, type=int)
    parser.add_argument('-a', '--addr', default='localhost')
    args = parser.parse_args()

    addr = args.addr
    port = args.port

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)

    while True:
        client, cl_addr = s.accept()
        message_in = client.recv(10240)
        try:
            message_raw = json.loads(message_in.decode('utf-8'))
        except Exception:
            message_raw = ''

        if message_raw:
            response = {
                "response": 200,
                "alert": "OK"
            }
        else:
            response = {
                "response": 400,
                "alert": "Bad Request"
            }
        message_json = json.dumps(response).encode('utf-8')
        try:
            client.send(message_json)
        except Exception:
            pass

        print(f'{cl_addr} : {message_raw}')
        print(response)
        client.close()


if __name__ == '__main__':
    main()
