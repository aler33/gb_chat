from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
# from sqlalchemy.orm import registry
from datetime import datetime

engine = create_engine('sqlite:///client_sqlite.db', echo=True, pool_recycle=7200)
metadata = MetaData()

users = Table('Users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(40), unique=True),
              Column('realname', String(40))
              )

users_history = Table('Users_history', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', ForeignKey('Users.id')),
                      Column('message', Text),
                      Column('time', DateTime)
                      )


# contacts = Table('Contacts', metadata,
#                  Column('id', Integer, primary_key=True),
#                  Column('contacts', ForeignKey('Users.id'))
#                  # contact = relationship('contacts', secondary='contacts_users', backref='contacts')
#                  )


class User:
    def __init__(self, name, realname=None):
        # print('=====================')
        self.id = None
        self.name = name
        self.realname = realname

    # def __repr__(self):
    #     return "<User ('%s','%s')>" % (self.name, self.realname)


class UsersHistory:
    def __init__(self, user, message, time):
        # print('99999999999999999999')
        self.id = None
        self.user = user
        self.message = message
        self.time = time


# class Contacts:
#     def __init__(self, contact):
#         self.contacts = contact
#

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

mapper(User, users)
mapper(UsersHistory, users_history)
# mapper(Contacts, contacts)


def add_users(name, message, realname=None):
    user_table = session.query(User).filter_by(name=name)
    if not user_table.count():
        user_new = User(name)
        session.add(user_new)
        session.commit()
    else:
        user_new = user_table.first()
        # session.query(UsersHistory).filter_by(user=user_new.id).update({'login_time': datetime.now()},
        #                                                                synchronize_session='fetch')

    print(user_new.id, datetime.now(), message)
    history = UsersHistory(user_new.id, message, datetime.now())
    session.add(history)

    session.commit()


def get_contact():
    list_contact = session.query(User)
    # print(f'USER == {user.id}')
    # list_contact = session.query(Contacts, User).filter_by(user=user.id).join(User, Contacts.contacts == User.id)

    return [user.name for user in list_contact]


# a = get_contact()
# print(a)
