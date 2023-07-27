from datetime import datetime, date, timedelta
import faker
from random import randint, choice
from pprint import pprint
from sqlalchemy import select

from src.models import Group, Teacher, Student, Discipline, Grade
from src.db import session

disciplines = [
    "Higher Mathematics",
    "Discrete Mathematics",
    "Linear Algebra",
    "Programming",
    "Theory of Probability",
    "History of Ukraine",
    "English",
    "Analytic Geometry"
]

groups = [
    'E331', 'TP-05-1', 'KN-51'
]

NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50

fake = faker.Faker()

def seed_teachers():
    # sql = 'INSERT INTO teachers (fullname) VALUES (?);'
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)
    session.commit()

def seed_disciplines():
    # sql = 'INSERT INTO disciplines (name, teacher_id) VALUES (?, ?);'
    teacher_ids = session.scalars(select(Teacher.id)).all()
    for discipline in disciplines:
        session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
    session.commit()

def seed_groups():
    # sql = 'INSERT INTO groups (name) VALUES (?);'
    for group in groups:
        session.add(Group(name=group))
    session.commit()

def seed_students():
    # sql = 'INSERT INTO students (fullname, group_id) VALUES (?, ?);'
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(NUMBER_STUDENTS):
            student = Student(fullname=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

def seed_grades():
    start_date = datetime.strptime('2022-09-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-06-15', '%Y-%m-%d')
    # sql = 'INSERT INTO grades (discipline_id, student_id, grade, date_of) VALUES (?, ?, ?, ?);'

    def get_list_date(start: date, end: date):
        result = []
        cur_date = start
        while cur_date <= end:
            if cur_date.isoweekday() < 6:
                result.append(cur_date)
            cur_date += timedelta(1)
        return result
    
    list_dates = get_list_date(start_date, end_date)

    discipline_ids = session.scalars(select(Discipline.id)).all()
    student_ids = session.scalars(select(Student.id)).all()

    for day in list_dates:
        r_disciplines = [choice(discipline_ids) for _ in range(3)]

        for discipline_id in r_disciplines:
            r_students = [choice(student_ids) for _ in range(4)]

            for student_id in r_students:
                grade = Grade(
                    grade=randint(2, 12),
                    date_of=day,
                    student_id=student_id,
                    discipline_id=discipline_id,
                )
                session.add(grade)
    session.commit()


if __name__ == '__main__':
    try:
        seed_teachers()
        seed_disciplines()
        seed_groups()
        seed_students()
        seed_grades()
    except Exception as err:
        pprint(err)

