from pprint import pprint
from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_01(params=[]):
    """
    --1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    SELECT g.student_id,
        s.fullname,
        ROUND(AVG(g.grade),2) avg_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id 
    GROUP BY g.student_id, s.fullname
    ORDER BY AVG(g.grade) DESC
    LIMIT 5; 
    """
    res = session.query(Student.id,
                        Student.fullname, 
                        func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
            .select_from(Grade) \
            .join(Student) \
            .group_by(Student.id) \
            .order_by(desc('avg_grade')) \
            .limit(5) \
            .all()
    return res

def select_02(params=[8]):
    """
    --2. Знайти студента із найвищим середнім балом з певного предмета.
    SELECT g.student_id,
        s.fullname,
        d.name discipline_name,
        ROUND(AVG(g.grade),2) avg_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id 
    JOIN disciplines d ON d.id  = g.discipline_id 
    WHERE 1=1
    AND d.id = :ID --8               -- код предмету
    GROUP BY g.student_id, s.fullname, d.name
    ORDER BY AVG(g.grade) DESC
    LIMIT 1;
    """
    discipline_id = params[0] if params else 8
    res = session.query(Grade.student_id, 
                        Student.fullname,
                        Discipline.name.label('discipline_name'),
                        func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
            .select_from(Grade) \
            .join(Student) \
            .join(Discipline) \
            .filter(Discipline.id == discipline_id) \
            .group_by(Grade.student_id, Student.fullname, Discipline.name) \
            .order_by(desc('avg_grade')) \
            .limit(1) \
            .all()
    return res

def select_03(params=[8]):
    """
    --3. Знайти середній бал у групах з певного предмета.
    SELECT s.group_id,
        gr.name group_name,
        d.name discipline_name,
        ROUND(AVG(g.grade),2) avg_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id 
    JOIN groups gr ON gr.id = s.group_id 
    JOIN disciplines d ON d.id  = g.discipline_id 
    WHERE 1=1
    AND d.id = 8               -- код предмету
    GROUP BY s.group_id, gr.name, d.name
    ORDER BY s.group_id, AVG(g.grade) DESC;
    """
    discipline_id = params[0] if params else 8
    res = session.query(Student.group_id,
                        Group.name.label('group_name'),
                        Discipline.name.label('discipline_name'),
                        func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
            .select_from(Grade) \
            .join(Student) \
            .join(Group) \
            .join(Discipline) \
            .filter(Discipline.id == discipline_id) \
            .group_by(Student.group_id, Group.name, Discipline.name) \
            .order_by(Student.group_id, desc('avg_grade')) \
            .all()
    return res


def select_04(params=[]):
    """
    --4. Знайти середній бал на потоці (по всій таблиці оцінок).
    SELECT ROUND(AVG(g.grade),2) avg_grade
    FROM grades g;
    """
    res = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
            .select_from(Grade)\
            .all()
    return res


def select_05(params=[4]):
    """
    --5. Знайти, які курси читає певний викладач.
    SELECT d.teacher_id,
        t.fullname teacher_name,
        d.name discipline_name
    FROM teachers t
    JOIN disciplines d ON d.teacher_id  = t.id 
    WHERE 1=1
    AND t.id = 4               -- код викладача
    ORDER BY d.teacher_id, d.id;
    """
    teacher_id = params[0] if params else 4

    res = session.query(Discipline.teacher_id,
                        Teacher.fullname.label('teacher_name'),
                        Discipline.name.label('discipline_name')) \
            .select_from(Teacher) \
            .join(Discipline) \
            .filter(Teacher.id == teacher_id) \
            .order_by(Discipline.teacher_id, Discipline.id) \
            .all()
    return res

def select_06(params=[1]):
    """
    --6. Знайти список студентів у певній групі.
    SELECT gr.name group_name,
        s.fullname 
    FROM students s 
    JOIN groups gr ON gr.id  = s.group_id 
    WHERE 1=1
    AND gr.id = 1              -- код групи
    ORDER BY gr.name , s.fullname;
    """
    group_id = params[0] if params else 1

    res = session.query(Group.name.label('group_name'),
                        Student.fullname) \
            .select_from(Student) \
            .join(Group) \
            .filter(Group.id == group_id) \
            .order_by(Group.name, Student.fullname) \
            .all()
    return res


def select_07(params=[8, 3]):
    """
    --7. Знайти оцінки студентів в окремій групі з певного предмета.
    SELECT s.group_id,
        gr.name group_name,
        d.name discipline_name,
        s.fullname,
        g.grade,
        g.date_of 
    FROM grades g
    JOIN students s ON s.id = g.student_id 
    JOIN groups gr ON gr.id = s.group_id 
    JOIN disciplines d ON d.id  = g.discipline_id 
    WHERE 1=1
    AND d.id = 8               -- код предмету
    AND gr.id = 3              -- код групи
    ORDER BY s.group_id, s.fullname, g.date_of;
    """
    discipline_id = params[0] if params else 8
    group_id = params[1] if params and len(params) == 2 else 3

    res = session.query(Student.group_id,
                        Group.name.label('group_name'),
                        Discipline.name.label('discipline_name'),
                        Student.fullname,
                        Grade.grade,
                        Grade.date_of) \
            .select_from(Grade) \
            .join(Student) \
            .join(Group) \
            .join(Discipline) \
            .filter(and_(Discipline.id == discipline_id, Group.id == group_id)) \
            .order_by(Student.group_id, Student.fullname, Grade.date_of) \
            .all()
    return res

def select_08(params=[4]):
    """
    --8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    SELECT d.teacher_id,
        t.fullname teacher_name,
        ROUND(AVG(g.grade),2) avg_grade
    FROM teachers t
    JOIN disciplines d ON d.teacher_id  = t.id 
    JOIN grades g ON g.discipline_id = d.id 
    WHERE 1=1
    AND t.id = 4               -- код викладача
    GROUP BY d.teacher_id, t.id 
    ORDER BY d.teacher_id, d.id;
    """
    teacher_id = params[0] if params else 4

    res = session.query(Discipline.teacher_id,
                        Teacher.fullname.label('teacher_name'),
                        func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
            .select_from(Teacher) \
            .join(Discipline) \
            .join(Grade) \
            .filter(Teacher.id == teacher_id) \
            .group_by(Discipline.teacher_id, Teacher.fullname) \
            .order_by(Discipline.teacher_id) \
            .all()
    return res

def select_09(params=[25]):
    """
    --9. Знайти список курсів, які відвідує студент.
    SELECT DISTINCT
        g.student_id,
        s.fullname,
        d.name discipline_name
    FROM students s  
    JOIN grades g ON g.student_id = s.id 
    JOIN disciplines d ON d.id = g.discipline_id 
    WHERE 1=1
    AND s.id = 25              -- код студента
    ORDER BY s.id, d.id;
    """
    student_id = params[0] if params else 25

    res = session.query(Grade.student_id,
                        Student.fullname,
                        Discipline.name.label('discipline_name')) \
            .select_from(Student) \
            .join(Grade) \
            .join(Discipline) \
            .filter(Student.id == student_id) \
            .group_by(Grade.student_id, Student.fullname, Discipline.name) \
            .order_by(Grade.student_id, Discipline.name) \
            .all()
    return res

def select_10(params= [25, 4]):
    """
    --10. Список курсів, які певному студенту читає певний викладач.
    SELECT DISTINCT
        g.student_id,
        s.fullname,
        t.fullname teacher_name,
        d.name discipline_name
    FROM students s  
    JOIN grades g ON g.student_id = s.id 
    JOIN disciplines d ON d.id = g.discipline_id
    JOIN teachers t ON t.id = d.teacher_id  
    WHERE 1=1
    AND s.id = 25              -- код студента
    AND t.id = 4               -- код викладача
    ORDER BY s.id, t.id,  d.id;
    """
    student_id = params[0] if params else 25
    teacher_id = params[1] if params and len(params) == 2 else 4

    res = session.query(Grade.student_id,
                        Student.fullname,
                        Teacher.fullname.label('teacher_name'),
                        Discipline.name.label('discipline_name')) \
            .select_from(Student) \
            .join(Grade) \
            .join(Discipline) \
            .join(Teacher) \
            .filter(and_(Student.id == student_id, Teacher.id == teacher_id)) \
            .group_by(Grade.student_id, Student.fullname, Teacher.fullname, Discipline.name) \
            .order_by(Grade.student_id, Teacher.fullname, Discipline.name) \
            .all()
    return res

def select_11(params= [4, 25]):
    """
    --11. Середній бал, який певний викладач ставить певному студентові.
    SELECT t.fullname teacher_name,
        s.fullname,
        ROUND(AVG(g.grade),2) avg_grade
    FROM teachers t 
    JOIN disciplines d ON d.teacher_id  = t.id
    JOIN grades g ON g.discipline_id  = d.id 
    JOIN students s ON s.id = g.student_id 
    WHERE 1=1
    AND t.id = 4               -- код викладача
    AND s.id = 25              -- код студента
    GROUP BY t.id, s.id
    ORDER BY t.id, s.id
    """
    teacher_id = params[0] if params else 4
    student_id = params[1] if params and len(params) == 2 else 25

    res = session.query(Teacher.fullname.label('teacher_name'),
                        Student.fullname,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
            .select_from(Teacher) \
            .join(Discipline) \
            .join(Grade) \
            .join(Student) \
            .filter(and_(Student.id == student_id, Teacher.id == teacher_id)) \
            .group_by(Teacher.fullname, Student.fullname) \
            .order_by(Teacher.fullname, Student.fullname) \
            .all()
    return res

def select_12(params=[1, 6]):
    """
    --12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    SELECT g.id group_id,
        g.name group_name,
        s.fullname,
        g3.discipline_id,
        g3.discipline_name,
        g3.max_date, 
        g2.grade
    FROM groups g 
    JOIN (
        SELECT g2.discipline_id,     -- предмети з останніми датами занять
                d.name discipline_name,
                MAX(g2.date_of) max_date
            FROM grades g2
            JOIN disciplines d ON d.id = g2.discipline_id
            where d.id = 6
            GROUP BY g2.discipline_id, d.name
    ) g3 on 1=1
    JOIN students s ON s.group_id  = g.id
    left join grades g2 on g2.student_id = s.id and g2.discipline_id = 6 AND g2.date_of = g3.max_date
    WHERE 1=1
    AND g.id = 1               -- код групи
    --AND g3.discipline_id = 6   -- код предмету
    ORDER BY g.id, grade, s.id;
    """
    group_id = params[0] if params else 1
    discipline_id = params[1] if params and len(params) == 2 else 6

    subquery_g3 = (select(Grade.discipline_id,
                          Discipline.name.label('discipline_name'),
                          func.max(Grade.date_of).label('max_date'))\
                    .join(Discipline) \
                    .where(Discipline.id == discipline_id)
                    .group_by(Grade.discipline_id, Discipline.name) 
                    .subquery('g3')
                )
    
    res = session.query(Student.group_id,
                        Group.name.label('group_name'),
                        Student.fullname,
                        subquery_g3.c.get('discipline_id').label('discipline_id'),
                        subquery_g3.c.get('discipline_name').label('discipline_name'),
                        subquery_g3.c.get('max_date').label('max_date'),
                        Grade.grade.label('grade')) \
            .select_from(subquery_g3) \
            .join(Group, Group.id == group_id) \
            .join(Student) \
            .outerjoin(Grade, and_(Grade.student_id == Student.id, Grade.discipline_id == discipline_id, Grade.date_of == subquery_g3.c.get('max_date'))) \
            .order_by(Student.group_id, Grade.grade, Student.fullname) \
            .all()
    return res


#     pprint(select_01())
#     pprint(select_02(8))
#     pprint(select_03(8))
#     pprint(select_04())
#     pprint(select_05(1))
#     pprint(select_06(1))
#     pprint(select_07(8, 3))
#     pprint(select_08(1))
#     pprint(select_09(25))
#     pprint(select_10(25, 1))
#     pprint(select_11(25, 1))
#     pprint(select_12(1, 6))

query = [
    [select_01],
    [select_02, ['код предмету', 8]], 
    [select_03, ['код предмету', 8]], 
    [select_04], 
    [select_05, ['код викладача', 4]], 
    [select_06, ['код групи', 1]], 
    [select_07, ['код предмету', 8], ['код групи', 3]], 
    [select_08, ['код викладача', 4]], 
    [select_09, ['код студента', 25]], 
    [select_10, ['код студента', 25], ['код викладача', 4]], 
    [select_11, ['код викладача', 4], ['код студента', 25]], 
    [select_12, ['код групи', 1], ['код предмету', 6]]
]

menu = """Виконати запит:
1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
2. Знайти студента із найвищим середнім балом з певного предмета.
3. Знайти середній бал у групах з певного предмета.
4. Знайти середній бал на потоці (по всій таблиці оцінок).
5. Знайти, які курси читає певний викладач.
6. Знайти список студентів у певній групі.
7. Знайти оцінки студентів в окремій групі з певного предмета.
8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
9. Знайти список курсів, які відвідує студент.
10. Список курсів, які певному студенту читає певний викладач.
11. Середній бал, який певний викладач ставить певному студентові.
12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
"""

text_input = 'Введіть номер запиту (0 або пусто - закінчення роботи) >>> '

def main():

    print(menu)
    list_menu = menu.split('\n')
    while True:
        try:
            inp = input(text_input)
            if not inp or inp == '0':
                break
            num = int(inp)
        except ValueError as err:
            print(err)
            continue
        
        if num < 1 or num > 12:
            print('Номер запиту повинен бути в інтервалі від 1 до 12!')
            continue
        
        list_query = query[num-1]
        params = []
        if len(list_query) > 1:
            for i in range(1, len(list_query)):
                par = list_query[i]
                while True:
                    s = 'Введіть ' + par[0] + ' [' + str(par[1]) + '] >> '
                    sn = input(s)
                    if sn:
                        if type(par[1]) == int:
                            try:
                                pn = int(sn)
                            except ValueError as err:
                                print(err)
                                continue
                            params.append(pn)
                        else:
                            params.append(sn)
                    else:
                        params.append(par[1])
                    break
        
        try:
            res = list_query[0](params)
            print(list_menu[num])
            for el in res:
                print(el)
        except Exception as err:
            print(err)
        
        input('Enter для продовження > ')
        print(menu)


if __name__ == '__main__':
    # pprint(select_01())
    # pprint(select_02(8))
    # pprint(select_03(8))
    # pprint(select_04())
    # pprint(select_05(1))
    # pprint(select_06(1))
    # pprint(select_07(8, 3))
    # pprint(select_08(4))
    # pprint(select_09(25))
    # pprint(select_10(25, 4))
    # pprint(select_11(1, 25))
    # pprint(select_12(1, 6))
    try:
        main()
    except Exception as err:
        print(err)


