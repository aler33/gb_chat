from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
import sys
import json
import logging
from time import time


from client_gui import Ui_MainClientWindow
from client_db import add_users, get_contact

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

    def select_active_user(self):
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

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
            add_users(contact_text, 'add_contact')
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
                    add_users(message['destination'], message['text'])
            except Exception:
                pass
            self.transport.send(message_json)

        except Exception:
            pass


    @pyqtSlot(str)
    def get_message(self):
        message_in = self.transport.recv(1024)
        message_raw = json.loads(message_in.decode('utf-8'))
        try:
            if message_raw['action'] == 'message':
                add_users(message_raw['user']['account_name'], message_raw['text'])
                self.ui.list_messages.setModel(message_raw)
        except Exception:
            pass

    def make_connection(self, trans_obj):
        trans_obj.new_message.connect(self.message)
