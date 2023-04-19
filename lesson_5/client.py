import logging
from socket import *
import json
import argparse
from time import time
import log.client_log_config


client_log = logging.getLogger('client')


def get_message(client):
    message_in = client.recv(1024)
    message_raw = json.loads(message_in.decode('utf-8'))
    client_log.info(f'get message from {client}')

    return message_raw


def processing_presence():
    client_log.info('message presence complete')
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
    client_log.info('message sent')


def processing_answer(message_raw):
    try:
        if message_raw['response'] and message_raw['alert']:
            client_log.info(f"processing answer {message_raw['response']} {message_raw['alert']}")
            return f"{message_raw['response']} {message_raw['alert']}"
    except Exception:
        client_log.warning('Bad server answer')
        return 'Bad server answer'


def main():

    try:
        client_log.info('start program')
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
        message_in = get_message(s)
        print(processing_answer(message_in))
    except ConnectionRefusedError:
        client_log.error('Error  Connection refused')
    except Exception:
        client_log.error('Error')

    client_log.info('program finished')
    s.close()


if __name__ == '__main__':
    main()
