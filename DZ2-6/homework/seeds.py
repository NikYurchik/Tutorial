from datetime import datetime, date, timedelta
import faker
from random import randint
import sqlite3
from pprint import pprint

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
connect = sqlite3.connect('homework.db')
cur = connect.cursor()

def seed_teachers():
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = 'INSERT INTO teachers (fullname) VALUES (?);'
    cur.executemany(sql, zip(teachers,))

def seed_disciplines():
    sql = 'INSERT INTO disciplines (name, teacher_id) VALUES (?, ?);'
    cur.executemany(sql, zip(disciplines, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(disciplines)))))

def seed_groups():
    sql = 'INSERT INTO groups (name) VALUES (?);'
    cur.executemany(sql, zip(groups,))

def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = 'INSERT INTO students (fullname, group_id) VALUES (?, ?);'
    cur.executemany(sql, zip(students, iter(randint(1, len(groups)) for _ in range(len(students)))))

def seed_grades():
    start_date = datetime.strptime('2022-09-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-06-15', '%Y-%m-%d')
    sql = 'INSERT INTO grades (discipline_id, student_id, grade, date_of) VALUES (?, ?, ?, ?);'

    def get_list_date(start: date, end: date):
        result = []
        cur_date = start
        while cur_date <= end:
            if cur_date.isoweekday() < 6:
                result.append(cur_date)
            cur_date += timedelta(1)
        return result
    
    list_dates = get_list_date(start_date, end_date)
    grades = []
    for day in list_dates:
        r_disciplines = [randint(1, len(disciplines)) for _ in range(3)]    # цикл по дисциплинам
        for discipline in r_disciplines:
            r_students = [randint(1, NUMBER_STUDENTS) for _ in range(4)]
            for student in r_students:
                grades.append((discipline, student, randint(2, 12), day.date()))
    cur.executemany(sql, grades)


if __name__ == '__main__':
    try:
        seed_teachers()
        seed_disciplines()
        seed_groups()
        seed_students()
        seed_grades()
        connect.commit()
    except sqlite3.Error as err:
        pprint(err)
    finally:
        connect.close()

