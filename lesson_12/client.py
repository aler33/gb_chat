from socket import *
import json
import argparse
from time import time
from threading import Thread
import log.client_log_config
import logging
import dis


client_log = logging.getLogger('client')


class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        list_methods = []
        for key, value in clsdict.items():
            try:
                gen = dis.get_instructions(value)
            except Exception:
                pass
            else:
                for instruct in gen:
                    if (instruct.opname == 'LOAD_GLOBAL') and (instruct.argval not in list_methods):
                        list_methods.append(instruct.argval)
        if ('accept' or 'listen') in list_methods:
            raise TypeError('Call accept or listen for socket')
        elif 'socket' in list_methods:
            raise TypeError('Create socket in class')
        if 'get_message' not in list_methods and 'send_message' not in list_methods:
            raise TypeError('There is no use of sockets for work on TCP')

        super().__init__(clsname, bases, clsdict)


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


class Read(Thread, metaclass=ClientVerifier):
    def __init__(self, client):
        self.client = client
        super().__init__()

    def run(self):
        while True:
            try:
                data = get_message(self.client)
                # data = json.loads(self.client.recv(1024).decode('utf-8'))
                # client_log.info(f'receive from server {data}')
                print(f"Message from {data['user']['account_name']} - {data['text']}")
            except:
                pass


class Send(Thread, metaclass=ClientVerifier):
    def __init__(self, client, username):
        self.client = client
        self.username = username
        super().__init__()

    def run(self):
        to_name = input('Enter destination name')
        print('Enter your message, "q" for quit :')
        while True:
            txt = input()
            if txt == 'q':
                return
            message = {
                'action': 'message',
                'time': time(),
                'type': 'message',
                'destination': to_name,
                'text': txt,
                'user': {
                    'account_name': self.username,
                    'status': 'I am here!'
            }
        }
            # message_json = json.dumps(message).encode('utf-8')
            # self.client.send(message_json)
            send_message(self.client, message)
            client_log.info(f'{message} sent to {self.client}')


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
        reading = Read(s)
        # reading = Thread(target=read_serv, args=(s,))
        reading.daemon = True
        if arg_receive == 1:
            if arg_send != 1:
                reading.daemon = False
            reading.start()

        sending = Send(s, user_name)
        # sending.daemon = True
        if arg_send == 1:
            sending.start()


if __name__ == '__main__':
    main()
