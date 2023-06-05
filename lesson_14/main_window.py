from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
import sys
import json
import logging
from time import time


from client_gui import Ui_MainClientWindow
from client_db import add_users, get_contact, get_history

client_log = logging.getLogger('client')


class ClientMainWindow(QMainWindow):
    def __init__(self, transport, user_name):
        super().__init__()

        self.user_name = user_name
        self.transport = transport

        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        self.ui.menu_exit.triggered.connect(qApp.exit)

        self.ui.btn_send.clicked.connect(self.send_message)

        self.ui.btn_add_contact.clicked.connect(self.add_contact)

        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        self.ui.label_new_message.setText('дважды кликните в окне контактов')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)


    def history_list_update(self):
        list = sorted(get_history(self.current_chat), key=lambda item: item[3])
        print('++++++++++++++++', list)
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        self.history_model.clear()
        length = len(list)
        start_index = 0
        if length > 20:
            start_index = length - 20
        for i in range(start_index, length):
            item = list[i]
            if item[1] == 'in':
                mess = QStandardItem(f'Входящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(f'Исходящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()
        self.history_list_update()

    def set_active_user(self):
        self.ui.label_new_message.setText(f'Введите сообщенние для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

    def clients_list_update(self):
        contacts_list = get_contact()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)
    #

    def add_contact(self):
        contact_text = self.ui.new_contact.toPlainText()
        self.ui.new_contact.clear()
        if not contact_text:
            return
        try:
            to_ = None
            add_users(contact_text, to_, 'add_contact')
            print(contact_text)

            contacts_list = get_contact()
            self.contacts_model = QStandardItemModel()
            for i in sorted(contacts_list):
                item = QStandardItem(i)
                item.setEditable(False)
                self.contacts_model.appendRow(item)
            self.ui.list_contacts.setModel(self.contacts_model)

        except Exception:
            pass

    def send_message(self):
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        try:
            message = {
                'action': 'message',
                'time': time(),
                'type': 'message',
                'destination': self.current_chat,
                'text': message_text,
                'user': {
                    'account_name': self.user_name,
                    'status': 'I am here!'
                }
            }
            message_json = json.dumps(message).encode('utf-8')
            try:
                if message['action'] == 'message':
                    to_ = 'to'
                    # print(f"THIS IS HISTORY!!!---=====--- {message['destination']}, {to_}, {message['text']}")
                    add_users(message['destination'], to_, message['text'])
                    # print(f"HISTORY!!!------ {message['destination']}, {to_}, {message['text']}")
                    a = get_history(message["destination"])
                    # print(f'THIS IS HISTORY!!!------ {a}')
                    self.history_list_update()
            except Exception:
                pass
            self.transport.send(message_json)

        except Exception:
            pass


    @pyqtSlot(str)
    def get_message(self):
        message_in = self.transport.recv(1024)
        message_raw = json.loads(message_in.decode('utf-8'))
        self.history_list_update()
        try:
            if message_raw['action'] == 'message':
                to_ = 'from'
                add_users(message_raw['user']['account_name'], to_, message_raw['text'])
                print(f'THIS IS HISTORY!!!------ {get_history(message_raw["user"])}')
                self.ui.list_messages.setModel(message_raw)
        except Exception:
            pass

    def make_connection(self, trans_obj):
        trans_obj.new_message.connect(self.message)
