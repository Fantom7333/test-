from datetime import date
from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey, create_engine
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///info_data_base.db', echo=True)
Base = declarative_base(bind=engine)

class Abstract:
    id = Column(Integer, primary_key=True)
    created_on = Column(Date, default=date.today())

class User(Abstract, Base):
    __tablename__ = 'users'
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(20), nullable=False)

    tasks = relationship("Task", cascade = "all, delete-orphan")

    def __str__(self):
        return " | ".join([self.id, self.username, self.email, self.password])

class Task(Abstract, Base):
    __tablename__ = 'tasks'
    title = Column(String(20), nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    details = Column(Text)
    deadline = Column(Date)
    status = Column(Boolean, default=0)

    author = relationship(User)
    def __str__(self):
        return ' | '.join([self.id, self.title, self.status])

Base.metadata.create_all()

def add_user(name, email, password):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = User(username=name , email=email , password=password)
    session.add(user)
    session.commit()
    session.close()

