"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой
узел должен быть представлен именем хоста или ip-адресом. В функции необходимо
перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
помощью функции ip_address().

"""
import ipaddress
import os


def host_ping(host_list):
    for adress in host_list:
        hostname = ipaddress.ip_address(adress)
        response = os.system('ping -c 1 ' + str(hostname))
        print(f'{adress} Reachable') if response == 0 else print(f'{adress} Unreachable')


if __name__ == '__main__':
    ip_list = ['192.168.1.1', '192.168.1.3', '192.168.1.10']
    host_ping(ip_list)
