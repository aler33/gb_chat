from socket import *
import json
import select
import argparse
import logging
import log.server_log_config


server_log = logging.getLogger('server_1')


def send_message(client, response):
    message_json = json.dumps(response).encode('utf-8')
    try:
        client.send(message_json)
        server_log.info(f'message {response} sent {client}')
    except Exception:
        pass


def read_request(clients, all_clients, messages):
    responses = {}

    for sock in clients:
        try:
            data = json.loads(sock.recv(1024).decode('utf-8'))
            responses[sock] = data
            server_log.info(f'from {sock} receiving {data}')

            # OLD CODE
            if 'action' in data and data['action'] == 'presence':
                response = {
                    "response": 200,
                    "alert": "OK"
                }
                server_log.info(f'response {response}')
                send_message(sock, response)
                return messages

            elif 'action' in data and data['action'] == 'message':
                messages.append(data)



            # NEW CODE
            return messages
        except:
            all_clients.remove(sock)

    # print(messages)
    return messages


def write_response(message, w_clients, all_clients):
    # print(message, '--==--', w_clients, '--', all_clients)
    for sock in all_clients:
        try:
            answ = json.dumps(message).encode('utf-8')
            sock.send(answ)
            server_log.info(f'message {message} sent')
        except:
            sock.close()
            all_clients.remove(sock)


def main():
    server_log.info('start program')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, type=int)
    parser.add_argument('-a', '--addr', default='localhost')
    args = parser.parse_args()

    addr = args.addr
    port = args.port

    clients = []
    messages = []

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    s.settimeout(0.2)

    while True:
        try:
            client, cl_addr = s.accept()
        except OSError as e:
            pass
        else:
            clients.append(client)
            server_log.info(f'connected from {cl_addr}')
        finally:
            wait = 1
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            messages = read_request(r, clients, messages)
            # print(messages)

            if messages:
                for msg in messages:
                    if msg:
                        write_response(msg, w, clients)
                        messages.remove(msg)


if __name__ == '__main__':
    main()
