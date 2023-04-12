from socket import *
import json
import argparse
from time import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr')
    parser.add_argument('-p', '--port', default=7777, type=int)
    args = parser.parse_args()
    print(args.addr, args.port)

    addr = args.addr if args.addr else 'localhost'
    port = args.port

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((addr, port))
    message = {
        "action": "presence",
        "time": time(),
        "type": "status",
        "user": {
            "account_name": "user0",
            "status": "I am here!"
        }
}

    message_json = json.dumps(message).encode('utf-8')
    s.send(message_json)

    try:
        message_in = s.recv(1024)
        message_raw = json.loads(message_in.decode('utf-8'))
        if message_raw['response'] and message_raw['alert']:
            print(f"{message_raw['response']} {message_raw['alert']}")

    except Exception:
        print('Bad server answer')

    s.close()


if __name__ == '__main__':
    main()
