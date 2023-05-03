"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса. По результатам проверки должно
выводиться соответствующее сообщение.

"""

import ipaddress
import os


def host_range_ping(host_start, number_range):
    ip_host = ipaddress.ip_address(host_start)
    good_list = []
    bad_list = []
    for numb in range(number_range):
        hostname = ipaddress.ip_address(ip_host + numb)
        response = os.system('ping -c 1 ' + str(hostname))
        print(f'{hostname} Reachable') if response == 0 else print(f'{hostname} Unreachable')
        good_list.append(str(hostname)) if response == 0 else bad_list.append(str(hostname))
    print(f'Reacheble hosts: {good_list} \nUnrecheble hosts: {bad_list}')


if __name__ == '__main__':
    ip_start = '192.168.1.1'
    numb_range = 15
    host_range_ping(ip_start, numb_range)
