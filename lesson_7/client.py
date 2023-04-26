from socket import *
# from select import select
import argparse
import log.client_log_config
import logging
import cl_read
import cl_send


client_log = logging.getLogger('client')


def main():
    client_log.info('start program')
    parser = argparse.ArgumentParser()
    parser.add_argument('addr')
    parser.add_argument('-p', '--port', default=7777, type=int)
    args = parser.parse_args()

    addr = args.addr if args.addr else 'localhost'
    port = args.port

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((addr, port))
        while True:
            chose = input('"q" - quit, "r" - read, "s" - send messages ')
            if chose == 'q':
                break
            elif chose == 'r':
                cl_read.read(s)
            elif chose == 's':
                cl_send.send(s)


if __name__ == '__main__':
    main()