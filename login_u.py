from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

engine = create_engine('sqlite:///info_data_base.db', echo=True)
Base = declarative_base(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    avatar = Column(String, default='peppa.png', nullable=False)
    login_act = Column(Integer, default=0, nullable=False )
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
    owner = relationship(User)
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


def request_entry(login):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    check = session.query(User.login_act).filter(User.login == login).first()[0]
    print(check)
    session.close()
    return check


def change_entry(oz, login):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    check = session.query(User.login_act).filter(User.login == login).first()[0]
    if oz == "вход":
        check = 1
        session.commit()
    elif oz == "выход":
        check = 0
        session.commit()
    session.close()

