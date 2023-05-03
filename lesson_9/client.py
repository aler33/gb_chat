from socket import *
import json
import argparse
from time import time
from threading import Thread
import log.client_log_config
import logging


client_log = logging.getLogger('client')


def processing_presence(username):
    client_log.info('message presence complete')
    return {
        'action': 'presence',
        'time': time(),
        'type': 'status',
        'text': 'Hello!',
        'user': {
            'account_name': username,
            'status': 'I am here!'
        }
    }


def send_message(s, message):
    message_json = json.dumps(message).encode('utf-8')
    s.send(message_json)
    client_log.info('message sent')


def processing_answer(message_raw):
    try:
        if message_raw['response'] == 200 and message_raw['alert']:
            client_log.info(f"processing answer {message_raw['response']} {message_raw['alert']}")
            return f"{message_raw['response']} {message_raw['alert']}"
        else:
            client_log.warning('Bad server answer')
            # print('ErrorServerAnswer')
            raise ConnectionError
    except Exception:
        client_log.warning('Bad server answer')
        print('ErrorServerAnswer')
        raise ConnectionError
        # return 'Bad server answer'


def get_message(client):
    message_in = client.recv(1024)
    message_raw = json.loads(message_in.decode('utf-8'))
    client_log.info(f'get message from {client}')

    return message_raw


def read_serv(client):
    while True:
        try:
            data = json.loads(client.recv(1024).decode('utf-8'))
            client_log.info(f'receive from server {data}')
            print(f"Message from {data['user']['account_name']} - {data['text']}")
        except:
            pass


def sending_msgs(client, username):
    print('Enter your message, "q" for quit :')
    while True:
        txt = input()
        if txt == 'q':
            return
        message = {
            'action': 'message',
            'time': time(),
            'type': 'message',
            'text': txt,
            'user': {
                'account_name': username,
                'status': 'I am here!'
        }
    }
        message_json = json.dumps(message).encode('utf-8')
        client.send(message_json)
        client_log.info(f'{message} sent to {client}')


def main():
    user_name = input("Enter Username ")
    client_log.info(f'start program with username {user_name}')
    parser = argparse.ArgumentParser()
    parser.add_argument('addr')
    parser.add_argument('-p', '--port', default=7777, type=int)
    parser.add_argument('-r', '--receive', default=1, type=int)
    parser.add_argument('-s', '--send', default=1, type=int)
    args = parser.parse_args()

    addr = args.addr if args.addr else 'localhost'
    port = args.port
    arg_send = args.send
    arg_receive = args.receive

    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((addr, port))
        client_log.info(f'{s}')
        message = processing_presence(user_name)
        send_message(s, message)
        message_in = get_message(s)
        answ = processing_answer(message_in)
    except:
        pass
    else:
        reading = Thread(target=read_serv, args=(s,))
        reading.daemon = True
        if arg_receive == 1:
            if arg_send != 1:
                reading.daemon = False
            reading.start()

        sending = Thread(target=sending_msgs, args=(s, user_name))
        # sending.daemon = True
        if arg_send == 1:
            sending.start()


if __name__ == '__main__':
    main()
