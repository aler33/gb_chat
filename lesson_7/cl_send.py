import logging
import log.client_log_config


client_log = logging.getLogger('client')


def send(client):
    while True:
        message = input('Enter your message, "q" for quit :')
        if message == 'q':
            return
        client.send(message.encode('utf-8'))
        client_log.info(f'{message} sent to {client}')
