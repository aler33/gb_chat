import logging
from logging.handlers import TimedRotatingFileHandler


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s ')
servers_log_hand = TimedRotatingFileHandler('log/server.log', when='w0')
servers_log_hand.setFormatter(formatter)


servers_log = logging.getLogger('server')
servers_log.setLevel(logging.INFO)
servers_log.addHandler(servers_log_hand)