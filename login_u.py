from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

engine = create_engine('sqlite:///info_data_base.db', echo=True)
Base = declarative_base(bind=engine)


class EntryCheck(Base):
    __tablename__ = 'check_entry'
    id = Column(Integer, primary_key=True)
    check = Column(Integer, default=0, nullable=False)
    def __str__(self):
        return self.check

class Login(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, unique=True)
    def __str__(self):
        return self.login

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    avatar = Column(String, default='peppa.png', nullable=False)
    progress = relationship("Progress", cascade="all, delete-orphan")

    def __str__(self):
        return " | ".join([self.id, self.username, self.email, self.password])


class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_tasks_completed = Column(Integer, nullable=False)
    score = Column(Integer)
    course_name = Column(Text(100), nullable=False, unique=True)
    total_tasks = Column(Integer, nullable=False)

    def __str__(self):
        return ' | '.join([self.id, self.user_id, self.total_tasks_completed, self.score])


Base.metadata.create_all()


def add_user(login, email, password):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = User(login=login, email=email, password=password)
    session.add(user)
    session.commit()
    session.close()


def request_user(login):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    password_valid = session.query(User.password).filter(User.login == login).first()[0]
    avatar = session.query(User.avatar).filter(User.login == login).first()[0]
    session.close()
    return password_valid, avatar, login


def request_entry():
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    check = session.query(EntryCheck.check).first()[0]
    print(check)
    session.close()
    return check


def change_entry(oz):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    check = session.query(EntryCheck.check).first()[0]
    if oz == "вход":
        check = 1
        session.commit()
    elif oz == "выход":
        check = 0
        session.commit()
    session.close()


def set_auth_attr(login):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user_login = session.query(Login.login).first()[0]
    user_login = login
    session.commit()
    session.close()

def get_login():
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user_login = session.query(Login.login).first()[0]
    session.close()
    return user_login


# РАСКОММЕНТИТЬ И ЗАПУСТИТЬ, КОГДА УДАЛЯЕТЕ БАЗУ ДАННЫХ
# session = Session(bind=engine)
# check = EntryCheck(check=0)
# session.add(check)
# session.commit()
# session.close()
#
# session = Session(bind=engine)
# login = Login(login="AYE88")
# session.add(login)
# session.commit()
# session.close()
