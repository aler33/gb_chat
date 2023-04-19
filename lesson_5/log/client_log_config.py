import logging


# logger = logging.getLogger('client')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s ')
clients_log_hand = logging.FileHandler('log/client.log')
clients_log_hand.setFormatter(formatter)


clients_log = logging.getLogger('client')
clients_log.setLevel(logging.INFO)
clients_log.addHandler(clients_log_hand)
