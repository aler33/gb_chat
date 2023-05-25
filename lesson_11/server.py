from socket import *
import json
import select
import argparse
import logging
import log.server_log_config
import dis
from server_db import add_users


server_log = logging.getLogger('server_1')


class ServerVerifier(type):
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
                    elif (instruct.opname == 'LOAD_ATTR') and (instruct.argval not in list_methods):
                        list_methods.append(instruct.argval)
        if 'connect' in list_methods:
            raise TypeError('Call connect for socket')
        if not ('SOCK_STREAM' in list_methods and 'AF_INET' in list_methods):
            raise TypeError('There is no use of sockets for work on TCPs')

        super().__init__(clsname, bases, clsdict)


class Sock:
    def __init__(self):
        self._values = {}

    def __set__(self, instance, value):
        if not value or not value > 0:
            value = 7777
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Server(metaclass=ServerVerifier):

    port = Sock()

    def __init__(self, addr, port_numb):
        self.addr = addr
        self.port = port_numb
        self.clients = []
        self.messages = []

    def main_server(self):
        print(f'Server start with port number {self.port}')
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.settimeout(0.2)
        self.sock = s
        self.sock.listen()

        while True:
            try:
                client, cl_addr = self.sock.accept()
            except OSError as e:
                pass
            else:
                self.clients.append(client)
                server_log.info(f'connected from {cl_addr}')
            finally:
                wait = 1
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except:
                    pass

                messages = self.read_request(r, self.clients, self.messages)
                # print(messages)

                if messages:
                    for msg in self.messages:
                        if msg:
                            self.write_response(msg, w, self.clients)
                            self.messages.remove(msg)

    def send_message(self, client, response):
        message_json = json.dumps(response).encode('utf-8')
        try:
            client.send(message_json)
            server_log.info(f'message {response} sent {client}')
        except Exception:
            pass

    def read_request(self, clients, all_clients, messages):
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

                    print(f"{data['user']['account_name']} - {clients}")
                    add_users(data['user']['account_name'], clients)

                    server_log.info(f'response {response}')
                    self.send_message(sock, response)
                    return messages

                elif 'action' in data and data['action'] == 'message':
                    self.messages.append(data)



                # NEW CODE
                return messages
            except:
                all_clients.remove(sock)

        # print(messages)
        return messages

    def write_response(self, message, w_clients, all_clients):
        # print(message, '--==--', w_clients, '--', all_clients)
        for sock in all_clients:
            try:
                answ = json.dumps(message).encode('utf-8')
                sock.send(answ)
                server_log.info(f'message {message} sent')
            except:
                self.sock.close()
                self.all_clients.remove(sock)





def main():
    server_log.info('start program')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, type=int)
    parser.add_argument('-a', '--addr', default='localhost')
    args = parser.parse_args()

    addr = args.addr
    port = args.port

    server = Server(addr, port)
    server.main_server()


if __name__ == '__main__':
    main()
