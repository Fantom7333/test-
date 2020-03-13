from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, backref
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from str_functions import to_camel_case
a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
engine = create_engine('sqlite:///info_data_base.db', echo=True)
Base = declarative_base(bind=engine)

class AccountExists(Exception):
    '''
    Authentification pair already in db
    '''

class AccountNotFound(Exception):
    '''
    Authentification pair not found in db
    '''

class CourseNotFound(Exception):
    '''
    This course does not exist
    '''

class SectionNotFound(Exception):
    '''
    This section does not exist
    '''

class ClassNotFound(Exception):
    '''
    This class does not exist
    '''

class CourseExist(Exception):
    '''
    This course already exist
    '''

class SectionExist(Exception):
    '''
    This section already exist
    '''

class ClassExist(Exception):
    '''
    This class already exist
    '''

class PartOfClassExist(Exception):
    '''
    This part of class already exist
    '''
class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(30), nullable=False, unique=True)
    avatar = Column(String, default='course.png', nullable=False)
    course_sections = relationship("CourseSection", cascade="all, delete-orphan")
    def __repr__(self):
        return str(self.sections)

class CourseSection(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    section_name = Column(String(30), nullable=False, unique=True)
    avatar = Column(String, default='course.png', nullable=False)
    course = relationship(Courses)
    classes = relationship("SectionClasses", cascade="all, delete-orphan")
    def __repr__(self):
        return " | ".join([self.section_name, str(self.id)])

class SectionClasses(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    class_name = Column(String(30), nullable=False, unique=True)
    avatar = Column(String, default='course.png', nullable=False)
    section = relationship(CourseSection)
    parts = relationship("PartOfClass", cascade="all, delete-orphan")
    def __repr__(self):
        return f'{self.class_name, str(self.id)}'
class PartOfClass(Base):
    __tablename__ = 'parts'
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    info = Column(String(1200), nullable=False, unique=True)
    valid_id = Column(Integer, nullable=False, default=0)
    test = Column(Boolean, nullable=False, default=False)
    classes = relationship(SectionClasses)
    def __repr__(self):
        return f'{self.info, self.test}'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    avatar = Column(String, default='peppa.png', nullable=False)
    login_act = Column(Integer, default=0, nullable=False)
    progress = relationship("Progress", cascade="all, delete-orphan")
    forgot_code = Column(String(10), nullable=False, unique=False, default=0)
    def __str__(self):
        return " | ".join([str(self.id), self.username, self.email, self.password])


class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_tasks_completed = Column(Integer, nullable=False)
    score = Column(Integer)
    course_name = Column(Text(100), nullable=False, unique=True)
    total_tasks = Column(Integer, nullable=False)
    last_course_point = Column(Integer, nullable=False)
    owner = relationship(User)
    def __str__(self):
        return ' | '.join([self.id, self.user_id, self.total_tasks_completed, self.score])







Base.metadata.create_all()

def add_user(login, email, password):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = User(login=login, email=email, password=generate_password_hash(password))
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        raise AccountExists(Exception)
    finally:
        session.close()

def request_user(login):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(login=login).first()
    session.close()
    if not user:
        raise AccountNotFound
    return user.login, user.password


def request_user_login(email):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(email=email).first()
    session.close()
    if not user:
        raise AccountNotFound
    return user.login

def check_user_by_email(email):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(email=email).first()
    session.close()
    if not user:
        raise AccountNotFound
    return email


def request_user_avatar(login):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    avatar = session.query(User.avatar).filter(User.login == login).first()[0]
    session.close()
    return avatar


def request_entry(login):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    check = session.query(User.login_act).filter(User.login == login).first()[0]
    print(check)
    session.close()
    return check



#При входе заносит 1 в поле login_act записи пользователя по его нику, при выходе 0. Позволяет отслеживать онлайн.
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


def get_user_tasks(login):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(login=login).first()
    user_tasks = user.progress
    session.close()
    return user_tasks

#Добавление кода восстановления в базу
def add_check_password(email):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(email=email).first()
    list_code = np.random.choice(a, 10).tolist()
    user.forgot_code = ''.join(list_code)
    code = user.forgot_code
    # print(code) для проверки
    session.commit()
    session.close()
    return code


def remove_check_password(email):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(email=email).first()
    code = user.forgot_code
    code = 0
    session.commit()
    session.close()


def get_check_password(email):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    code = session.query(User.forgot_code).filter_by(email=email).first()[0]
    session.close()
    return code


def change_user_password(email, password_new):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(email=email).first()
    user.password = generate_password_hash(password_new)
    session.commit()
    session.close()


#Получение данных



def get_courses():
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    courses = session.query(Courses.course_name, Courses.avatar).all()
    if not id:
        raise CourseNotFound
    session.close()
    print(courses)
    return courses



def get_sections(course):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    course = session.query(Courses).filter_by(course_name=course).first()
    try:
        sections = course.course_sections
    except AttributeError:
        raise CourseNotFound
    session.close()
    print(sections)
    return sections


def get_classes(course, section):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    course = session.query(Courses).filter_by(course_name=course).first()
    try:
        sections = course.course_sections
    except AttributeError:
        raise CourseNotFound
    try:
        section_act = [i for i in sections if i.section_name == section][0]
    except IndexError:
        raise SectionNotFound
    classes = section_act.classes
    session.close()
    print(classes)
    return classes



def get_parts_of_class(course, section, class_name):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    course = session.query(Courses).filter_by(course_name=course).first()
    try:
        sections = course.course_sections
    except AttributeError:
        raise CourseNotFound
    try:
        section_act = [i for i in sections if i.section_name == section][0]
    except IndexError:
        raise SectionNotFound
    classes = section_act.classes
    try:
        class_act = [i for i in classes if i.class_name == class_name][0]
    except IndexError:
        raise ClassNotFound
    parts = class_act.parts
    session.close()
    print(parts)
    return parts



#Добавление данных в таблицу с курсами


def set_course(course, avatar=None):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    course= to_camel_case(course)
    if avatar:
        course_new = Courses(course_name=course, avatar=avatar)
    else:
        course_new = Courses(course_name=course)
    try:
        session.add(course_new)
        session.commit()
    except IntegrityError:
        raise CourseExist
    session.close()

def set_sections(course, section, avatar=None):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    #Информация о наличии пробелов в названии курса не нужна, тк создём секцию. Далее так же в других функциях.
    course = to_camel_case(course)
    section = to_camel_case(section)
    course = session.query(Courses).filter_by(course_name=course).first()
    try:
        sections = course.course_sections
    except AttributeError:
        raise CourseNotFound
    if avatar:
        section_new = CourseSection(section_name=section, avatar=avatar)
    else:
        section_new = CourseSection(section_name=section)
    try:
        sections.append(section_new)
        session.commit()
    except IntegrityError:
        raise SectionExist
    session.close()





def set_class(section, class_name, avatar=None):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    section = to_camel_case(section)
    class_name = to_camel_case(class_name)
    section = session.query(CourseSection).filter_by(section_name=section).first()
    try:
        classes = section.classes
    except AttributeError:
        raise SectionNotFound
    if avatar:
        class_new = SectionClasses(class_name=class_name, avatar=avatar)
    else:
        class_new = SectionClasses(class_name=class_name)
    try:
        classes.append(class_new)
        session.commit()
    except IntegrityError:
        raise ClassExist
    session.close()

def set_part_of_class(class_name, info, valid_id=0, test=False):
    engine = create_engine('sqlite:///info_data_base.db', echo=True)
    session = Session(bind=engine)
    class_name = to_camel_case(class_name)
    class_act = session.query(SectionClasses).filter_by(class_name=class_name).first()
    try:
        parts = class_act.parts
    except AttributeError:
        raise ClassNotFound
    if test:
        part_new = PartOfClass(info=info, test=test, valid_id=valid_id)
    elif not test:
        part_new = PartOfClass(info=info)
    try:
        parts.append(part_new)
        session.commit()
    except IntegrityError:
        raise PartOfClassExist
    session.close()


# get_sections("Python")
# get_parts_of_class("Python", "ВведениеВPython3", 'Объекты')

# Для теста. Раскоменчивать и запускать после удаления БД.
# set_course("Python")
# set_sections("Python", "Введение В Python3")
# set_sections("Python", "ООП")
# set_class("Введение В Python3", "Объекты")
# set_class("Введение В Python3", "Типы данных")
# set_class("ООП", "Введение в ООП")
# set_class("ООП", "Атрибуты")
# set_part_of_class("Объекты", "Элментарная единица информации: Объект, Кластер, Переменная", test = True, valid_id=1)
# set_part_of_class("Объекты", "Объекты в ЯП прикрепляются к переменным-ссылкам")
# set_part_of_class("Типы данных", "Разновидности типов данных")
# set_part_of_class("Типы данных", "String, float, int...")
# set_part_of_class("Введение в ООП", "3 главных понятия: Наследование, Инкапсуляция, Полиморфизм")
# set_part_of_class("Введение в ООП", "Полиморфизм - изменение свойств родительского класса в дочернем")
# set_part_of_class("Атрибуты", "Выберите вариант ответа: Переменная, Класс, Список", test = True, valid_id=3)
# set_part_of_class("Атрибуты", "Атрибуты - именованные свойства объекта")