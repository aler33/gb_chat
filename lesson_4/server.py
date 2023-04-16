from socket import *
import json
import argparse


def get_message(client):
    message_in = client.recv(10240)
    try:
        message_raw = json.loads(message_in.decode('utf-8'))
    except Exception:
        message_raw = ''
    return message_raw


def processing_message(message):
    if message:
        if message['action'] == 'presence':
            response = {
                "response": 200,
                "alert": "OK"
            }
        else:
            response = {
                "response": 404,
                "alert": "Not Found"
            }
    else:
        response = {
            "response": 400,
            "alert": "Bad Request"
        }
    return response


def send_message(client, response):
    message_json = json.dumps(response).encode('utf-8')
    try:
        client.send(message_json)
    except Exception:
        pass


def main():
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
            message_raw = get_message(client)
            print(f'{cl_addr} : {message_raw}')
            response = processing_message(message_raw)
            print(response)
            send_message(client, response)
        except Exception:
            pass

        client.close()


if __name__ == '__main__':
    main()
