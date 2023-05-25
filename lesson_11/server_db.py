from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DATETIME
from sqlalchemy.orm import mapper, sessionmaker
# from sqlalchemy.orm import registry
from datetime import datetime

engine = create_engine('sqlite:///sqlite.db', echo=True, pool_recycle=7200)
metadata = MetaData()

users = Table('Users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(40), unique=True),
              Column('realname', String(40))
              )

users_history = Table('Users_history', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', ForeignKey('Users.id')),
                      Column('login_time', DATETIME),
                      Column('address', String(30))
                      )

contacts_users = Table('Contacts_users', metadata,
                       Column('user', Integer, ForeignKey('Users.id')),
                       Column('contacts', Integer, ForeignKey('Users.id')),
                       )

contacts = Table('Contacts', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user', ForeignKey('Users.id')),
                 Column('contacts', ForeignKey('Users.name')),
                 # contact = relationship('contacts', secondary='contacts_users', backref='contacts')
                 )


class User:
    def __init__(self, name, realname=None):
        print('=====================')
        self.id = None
        self.name = name
        self.realname = realname

    # def __repr__(self):
    #     return "<User ('%s','%s')>" % (self.name, self.realname)


class UsersHistory:
    def __init__(self, user, login_time, address):
        print('99999999999999999999')
        self.id = None
        self.user = user
        self.login_time = login_time
        self.address = address


class Contacts:
    def __init__(self, user, contact):
        self.user = user
        self.contact = contact


metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

mapper(User, users)
mapper(UsersHistory, users_history)
mapper(Contacts, contacts)


def add_users(name, address, realname=None):
    user_table = session.query(User).filter_by(name=name)
    if not user_table.count():
        user_new = User(name)
        session.add(user_new)
        session.commit()
    else:
        user_new = user_table.first()

    session.query(UsersHistory).filter_by(user=user_new.id).update({'login_time': datetime.now()},
                                                                   synchronize_session='fetch')

    session.commit()
