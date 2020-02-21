from datetime import date
from sqlalchemy import (Column, Integer, String, Boolean, Text, Date, ForeignKey, create_engine)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base(bind=engine)



class Main(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    progress = relationship("Progress", cascade="all, delete-orphan")
    
    def __str__(self):
        return " | ".join([self.id, self.username, self.email, self.password])


class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_tasks_completed = Column(Integer, nullable=False)
    score = Column(Integer(1))
    course_name = Column(Text(100), nullable=False, unique=True)
    total_tasks = Column(Integer, nullable=False)

    def __str__(self):
        return ' | '.join([self.id, self.user_id, self.total_tasks_completed, self.score])


Base.metadata.create_all()


def add_user(name, email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = Main(username=name, email=email, password=password)
    session.add(user)
    session.commit()
    session.close()
