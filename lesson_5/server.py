from socket import *
import json
import argparse
import logging
import log.server_log_config


server_log = logging.getLogger('server')


def get_message(client):
    message_in = client.recv(10240)
    try:
        message_raw = json.loads(message_in.decode('utf-8'))
    except Exception:
        message_raw = ''
    return message_raw


def processing_message(message):
    if message:
        try:
            message['action']
        except Exception:
            server_log.warning("no field 'action'")
            return {
                "response": 400,
                "alert": "Bad Request"
            }
        if message['action'] == 'presence':
            response = {
                "response": 200,
                "alert": "OK"
            }
            server_log.info(f'response {response}')
        else:
            server_log.warning("'action' not 'present'")
            response = {
                "response": 404,
                "alert": "Not Found"
            }
    return response


def send_message(client, response):
    message_json = json.dumps(response).encode('utf-8')
    try:
        client.send(message_json)
    except Exception:
        pass


def main():
    server_log.info('start program')
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
        try:
            server_log.info(f'connecting from {cl_addr}')
            message_raw = get_message(client)
            server_log.info(f'{cl_addr} : {message_raw}')
            response = processing_message(message_raw)
            print(response)
            send_message(client, response)
            server_log.info('message sent')
        except Exception:
            server_log.error('error - something went wrong')

        server_log.info('client finished')
        client.close()


if __name__ == '__main__':
    main()
