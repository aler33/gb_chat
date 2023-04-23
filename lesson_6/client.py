import logging
from socket import *
import json
import argparse
from time import time
import log.client_log_config
import inspect


client_log = logging.getLogger('client')
client_log_new = logging.getLogger('client_1')


def log(func):
    def decorator(*args, **kwargs):
        client_log_new.info(f'called function -{func.__name__}- with args -{args}-, kwargs -{kwargs}- '
                            f'from function -{inspect.currentframe().f_back.f_code.co_name}-')
        fun = func(*args, **kwargs)
        return fun
    return decorator


@log
def get_message(client):
    message_in = client.recv(1024)
    message_raw = json.loads(message_in.decode('utf-8'))
    client_log.info(f'get message from {client}')

    return message_raw


@log
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


@log
def send_message(s, message):
    message_json = json.dumps(message).encode('utf-8')
    s.send(message_json)
    client_log.info('message sent')


@log
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
        client_log.info(f'{s}')
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
