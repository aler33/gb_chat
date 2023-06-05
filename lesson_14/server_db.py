from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import mapper, sessionmaker
# from sqlalchemy.orm import registry
from datetime import datetime

engine = create_engine('sqlite:///sqlite.db', echo=True, pool_recycle=7200)
metadata = MetaData()

users = Table('Users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(40), unique=True),
              Column('passwd', String(64)),
              Column('realname', String(40))
              )

users_history = Table('Users_history', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', ForeignKey('Users.id')),
                      Column('login_time', DateTime),
                      Column('address', String(200))
                      )

contacts_users = Table('Contacts_users', metadata,
                       Column('user', ForeignKey('Users.id')),
                       Column('contacts', ForeignKey('Users.id')),
                       )

contacts = Table('Contacts', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user', ForeignKey('Users.id')),
                 Column('contacts', ForeignKey('Users.id')),
                 # contact = relationship('contacts', secondary='contacts_users', backref='contacts')
                 )


class User:
    def __init__(self, name, passwd, realname=None):
        # print('=====================')
        self.id = None
        self.name = name
        self.passwd = passwd
        self.realname = realname

    # def __repr__(self):
    #     return "<User ('%s','%s')>" % (self.name, self.realname)


class UsersHistory:
    def __init__(self, user, login_time, address):
        self.id = None
        self.user = user
        self.login_time = login_time
        self.address = address


class Contacts:
    def __init__(self, user, contact):
        self.user = user
        self.contacts = contact


metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

mapper(User, users)
mapper(UsersHistory, users_history)
mapper(Contacts, contacts)


def add_users(name, address, passwd=None, realname=None):
    # print(f'address = {address}, len = {len(address)},,, {type(address)}')
    user_table = session.query(User).filter_by(name=name)
    if not user_table.count():
        user_new = User(name, passwd)
        session.add(user_new)
        session.commit()
    else:
        user_new = user_table.first()
        # session.query(UsersHistory).filter_by(user=user_new.id).update({'login_time': datetime.now()},
        #                                                                synchronize_session='fetch')
    # print(f'address = {address}, len = {len(address)},,, {type(address)}')
    # print(f'user_new.id = {user_new.id}')
    # print(user_new.id, datetime.now(), address)
    history = UsersHistory(user_new.id, datetime.now(), address)
    session.add(history)

    session.commit()


def add_contact(from_name, to_name):
    from_user = session.query(User).filter_by(name=from_name).first()
    contact = session.query(User).filter_by(name=to_name).first()
    if not from_user or not contact or session.query(Contacts).filter_by(user=from_name, contacts=to_name).count():
        return
    new_contact = Contacts(from_user.id, contact.id)
    session.add(new_contact)
    session.commit()


def get_contact(from_name):
    user = session.query(User).filter_by(name=from_name).one()
    print(f'USER == {user.id}')
    list_contact = session.query(Contacts, User).filter_by(user=user.id).join(User, Contacts.contacts == User.id)

    return [contacts[1].name for contacts in list_contact.all()]


def del_contact(from_name, to_name):
    from_user = session.query(User).filter_by(name=from_name).first()
    contact = session.query(User).filter_by(name=to_name).first()
    if not from_user or not contact:
        return
    session.query(Contacts).filter(Contacts.user == from_user.id, Contacts.contacts == contact.id).delete()
    print(f'DELETE!!!')
    session.commit()


def get_users():
    list_users = session.query(User)
    # print(f'USER == {user.id}')
    # list_contact = session.query(Contacts, User).filter_by(user=user.id).join(User, Contacts.contacts == User.id)

    return [user.name for user in list_users]


def get_hash(name):
    user = session.query(User).filter_by(name=name).first()
    print('10101010101')
    return user.passwd


if __name__ == '__main__':
    print(get_users())
    print(get_hash('alex'))
