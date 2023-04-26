from socket import *
import select
import argparse
import logging
import log.server_log_config


server_log = logging.getLogger('server')


def read_request(clients, all_clients):
    responses = {}

    for sock in clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
            server_log.info(f'from {sock} receiving {data}')
            return data
        except:
            all_clients.remove(sock)

    return ''


def write_response(requests, w_clients, all_clients):
    print(w_clients, '--', all_clients)
    for msg in requests:
        for sock in all_clients:
            try:
                answ = msg.encode('utf-8')
                print(answ)
                sock.send(answ)
            except:
                sock.close()
                all_clients.remove(sock)
        requests.remove(msg)


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
        finally:
            wait = 1
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_request(r, clients)
            if requests:
                messages.append(requests)
                print('00000000', requests)
                write_response(messages, w, clients)


if __name__ == '__main__':
    main()
