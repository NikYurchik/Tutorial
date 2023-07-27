from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.db import Base


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    # group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    group_id = Column(ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship(Group, backref='students')

class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship(Teacher, backref='disciplines')

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(Date, nullable=False)
    discipline_id = Column(Integer, ForeignKey('disciplines.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    discipline = relationship('Discipline', backref='grade')
    student = relationship('Student', backref='grade')


