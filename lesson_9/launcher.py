import subprocess
from threading import Thread


clients = {}
process = []


def creating_clients(s='-s1', r='-r1'):
    p = subprocess.call(['python', 'client.py', 'localhost', s, r], creationflags=subprocess.CREATE_NEW_CONSOLE)


while True:
    chose = input("Enter 'r' for receiving data;\nEnter 's' for sending data;\nEnter 'a' for all action;\n"
                  "Enter 'm' for multicliens;\n")
    if chose == 'a':
        client1 = Thread(target=creating_clients, args=('-s0', '-r1'))
        client1.daemon = True
        client1.start()
        client2 = Thread(target=creating_clients, args=('-s1', '-r0'))
        client2.daemon = True
        client2.start()
    elif chose == 'r':
        p = subprocess.call(['python', 'client.py', 'localhost', '-s0'])
    elif chose == 's':
        p = subprocess.call(['python', 'client.py', 'localhost', '-r0'])
    elif chose == 'm':
        try:
            number_clients = int(input('Enter number clients:\n'))
        except:
            number_clients = 2
        if 0 < number_clients < 10:
            print(number_clients)
            for numb in range(number_clients):
                clients[numb] = Thread(target=creating_clients)
                clients[numb].daemon = True
                clients[numb].start()
