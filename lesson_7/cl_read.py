import logging
import log.client_log_config


client_log = logging.getLogger('client')


def read(client):
    while True:
        data = client.recv(1024).decode('utf-8')
        client_log.info(f'receive from server {data}')
        print('Answer: ', data)

