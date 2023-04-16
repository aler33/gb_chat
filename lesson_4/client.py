from socket import *
import json
import argparse
from time import time


def get_message(client):
    message_in = client.recv(1024)
    message_raw = json.loads(message_in.decode('utf-8'))
    return message_raw


def processing_presence():
    return {
        'action': 'presence',
        'time': time(),
        'type': 'status',
        'user': {
            'account_name': 'user0',
            'status': 'I am here!'
        }
    }


def send_message(s, message):
    message_json = json.dumps(message).encode('utf-8')
    s.send(message_json)


def processing_answer(message_raw):
    try:
        if message_raw['response'] and message_raw['alert']:
            return f"{message_raw['response']} {message_raw['alert']}"
    except Exception:
        return 'Bad server answer'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr')
    parser.add_argument('-p', '--port', default=7777, type=int)
    args = parser.parse_args()

    addr = args.addr if args.addr else 'localhost'
    port = args.port

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((addr, port))
    message = processing_presence()
    send_message(s, message)

    try:
        message_in = get_message(s)
        print(processing_answer(message_in))
    except Exception:
        pass

    s.close()


if __name__ == '__main__':
    main()
