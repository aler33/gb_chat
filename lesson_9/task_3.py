"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из
примера 2. Но в данном случае результат должен быть итоговым по всем ip-адресам,
представленным в табличном формате (использовать модуль tabulate). Таблица должна
состоять из двух колонок и выглядеть примерно так
"""

import ipaddress
import os
from tabulate import tabulate
from itertools import zip_longest


def host_range_ping_tab(host_start, number_range):
    ip_host = ipaddress.ip_address(host_start)
    good_list = []
    bad_list = []
    for numb in range(number_range):
        hostname = ipaddress.ip_address(ip_host + numb)
        response = os.system('ping -c 1 ' + str(hostname))
        good_list.append(str(hostname)) if response == 0 else bad_list.append(str(hostname))
    hosts_list = list(zip_longest(good_list, bad_list, fillvalue=''))
    columns = ['Reachable', 'Unreachable']
    print(tabulate(hosts_list, headers=columns, tablefmt="grid"))


if __name__ == '__main__':
    ip_start = '192.168.1.1'
    numb_range = 15
    host_range_ping_tab(ip_start, numb_range)
