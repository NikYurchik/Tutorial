import sqlite3

query = [
    ['query_01.sql'],
    ['query_02.sql', ['код предмету', 8]], 
    ['query_03.sql', ['код предмету', 8]], 
    ['query_04.sql'], 
    ['query_05.sql', ['код викладача', 4]], 
    ['query_06.sql', ['код групи', 1]], 
    ['query_07.sql', ['код предмету', 8], ['код групи', 3]], 
    ['query_08.sql', ['код викладача', 4]], 
    ['query_09.sql', ['код студента', 25]], 
    ['query_10.sql', ['код студента', 25], ['код викладача', 4]], 
    ['query_11.sql', ['код викладача', 4], ['код студента', 25]], 
    ['query_12.sql', ['код групи', 1], ['код предмету', 6]]
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

connect = None

def main():

    def exec_query(sql, params):
        if params:
            cr = cur.execute(sql, params)
        else:
            cr = cur.execute(sql)
        res = cr.fetchall()
        return res

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
        
        with open(list_query[0], 'r') as fq:
            sql = fq.read()

        try:
            cur = connect.cursor()
            res = exec_query(sql, params)
            print(list_menu[num])
            for el in res:
                print(el)
        except sqlite3.Error as err:
            print(err)
        finally:
            cur.close()
        
        input('Enter для продовження > ')
        print(menu)


if __name__ == '__main__':
    connect = sqlite3.connect('homework.db')
    try:
        main()
    except Exception as err:
        print(err)
    finally:
        connect.close()

