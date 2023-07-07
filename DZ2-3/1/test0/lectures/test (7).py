# from datetime import datetime, timezone, timedelta, MINYEAR, date

# random_date = datetime(year=2022, month=5, day=11, hour=19, minute=36, second=30)

# print(random_date)
# print(random_date.date())
# print(random_date.time())

# print(datetime.now(tz=timezone.utc))
# print(datetime.today())

# td = "11.05.2022"
# d = datetime.strptime(td, "%d.%m.%Y")  # %y = 22; %Y = 2022
# print(d.date().strftime("%d.%m.%Y"))
# print(d.year, d.month, d.day, d.minute)

# other_d = d.replace(month=4, day=13, hour=14, minute=23, second=12)
# print(other_d)
# str_d = other_d.strftime("%Y/%d/%m %H:%M:%S")
# print(str_d)

"""
Клас datetime.timedelta - різниця між двома моментами часу, з точністю до мікросекунд.
Розглянемо наступну задачу. Наприклад, лікар прописала пацієнту приймати ліки протягом 45 днів.
Треба знайти дату закінчення прийому ліків від поточної дати.
"""
# d = datetime.now()
# interval = timedelta(days=45, hours=1)
# finish_d = d + interval
# print(finish_d)

# d = datetime.now()
# print(MINYEAR)
# print(d.timestamp()) # кількість секунд з 01.01.1970
# day = d.toordinal() # кількість днів з 01.01.01

# print(d.ctime())
# print(d)
# iso = d.isoformat()
# print(iso)
# sec = str(d.timestamp())

# restore_d_from_day = datetime.fromordinal(day)
# restore_d_from_iso = datetime.fromisoformat(iso)
# restore_d_from_sec = datetime.fromtimestamp(float(sec))

# print(restore_d_from_day)
# print(restore_d_from_iso)
# print(restore_d_from_sec)

# d1 = datetime(year=2021, month=1, day=1, hour=5)
# d_now = datetime.now()

# diff = d_now.timestamp() - d1.timestamp()
# print(diff)

# d_next = datetime.fromtimestamp(d_now.timestamp() + diff)
# print(d_next)

# interval = timedelta(days=180)
# d_next2 = d_now + interval
# print(d_next2)

"""
Напишіть функцію, що приймає на вхід три цілих числа: день, місяць і рік. Функція повинна повертати порядковий номер заданого дня у вказаному році.

Результат функції: номер року і порядковий номер дня в цьому році – обидва в цілочисельному форматі.
"""

# def transform_to_ordinal_date(day, month, year):
#     d = date(year, month, day).toordinal()
#     diff = d - date(year, 1, 1).toordinal() + 1
#     # print(d, date(year, 1, 1).toordinal())
#     return year, diff

# print(transform_to_ordinal_date(19, 1, 2022))
# print(transform_to_ordinal_date(31, 12, 2020))

"""
Зробіть функцію, що приймає в якості єдиного параметру порядкову дату, що має в собі рік і день 
по порядку. В якості результату функція повинна повертати день і місяць, що відповідають переданій порядковій даті.
"""
# def transform_to_date(ordinal, year):
#     d1 = date(year, 1, 1).toordinal()
#     d = datetime.fromordinal(d1 - 1 + ordinal)
#     return d

# print(transform_to_date(19, 2022))
# print(transform_to_date(366, 2020))
# print(transform_to_date(99, 2001))

# Написати функцію, що визначає який день тижня в певній даті у вигляді "день-місяць-рік".

# days_name = {
#     0: "понеділок",
#     1: "вівторок",
#     2: "середа",
#     3: "четвер",
#     4: "п'ятница",
#     5: "субота",
#     6: "неділя"
# }

# def day_of_week(my_date):
#     d, m, y =my_date.split("-")
#     parsed_date = datetime(day=int(d), month=int(m), year=int(y))
#     d_name = days_name.get(parsed_date.weekday())
#     return d_name

# print(day_of_week('31-05-2004'))
# print(day_of_week('26-05-1990'))
# print(day_of_week('10-12-1980'))
# print(day_of_week('11-04-1972'))
# print(day_of_week('17-05-2023'))

# import random

# print(random.random())
# print(random.randint(1, 10))

# for _ in range(10):
#     print(random.randint(1, 10), end=" ") # включає 10
    # print(random.randrange(1, 10), end=" ") # не включає 10

# l = list(range(1, 37))
# print(l)

# random.shuffle(l)
# print(l)

# print(random.choice(l))
# print(random.sample(l, k=5))

"""
Яку мінімальну кількість разів Ви маєте підкинути монетку, щоб три рази підряд випав або орел, або решка?
random.randint(A, B) - випадкове ціле число N, A ≤ N ≤ B.
"""

# d = {
#     1: "Орел",
#     2: "Решка"
# }

# count_O = 0
# count_P = 0

# sequence = []

# while count_P < 3 and count_O < 3:
#     trial = random.randint(1, 2)
#     if trial == 1:
#         count_O += 1
#         count_P = 0
#     else:
#         count_O = 0
#         count_P += 1
#     sequence.append(d[trial])

# print(sequence)
# print(f"3 times {d[1] if count_O == 3 else d[2]}")
# print(len(sequence))

"""
Генерування автомобільного знаку. Дві літери, чотири цифри, дві літери.
Для Kиївської облacті код АI
Останні дві літери зі списку: A, B, C, E, H, I, K, M, O, P, T, X
(використовуються українські літери, що мають графічні відповідники у латиниці)
"""

# start = "AI"
# set_of_letters = ["A", "B", "C", "E", "H", "I", "K", "M", "O", "P", "T", "X"]
# set_of_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# numbers = "".join(random.choices(set_of_numbers, k=4))
# print(numbers)
# last_l = "".join(random.choices(set_of_letters, k=2))

# print(f"{start} {numbers} {last_l}")

"""
Виконати симулювання 1000 викидів гральних кубиків. Порівняти очікуваний результат ймовірності випадання з реальним. Очікуваний:
2: 2,78
3: 5,56
4: 8,33
5: 11,11
6: 13,89
7: 16,67
8: 13,89
9: 11,11
10: 8,33
11: 5,56
12: 2,78
Результат зберігати в текстовий файл формату md, у вигляді таблиці. Показати.
"""

# NUMBER_ATTEMPTS = 1000

# expected_outcome = {
#     "2": 2.78,
#     "3": 5.56,
#     "4": 8.33,
#     "5": 11.11,
#     "6": 13.89,
#     "7": 16.67,
#     "8": 13.89,
#     "9": 11.11,
#     "10": 8.33,
#     "11": 5.56,
#     "12": 2.78
# }

# def dice_roll():
#     return random.randint(1, 6)

# def experiment():
#     values = {
#         "2": 0,
#         "3": 0,
#         "4": 0,
#         "5": 0,
#         "6": 0,
#         "7": 0,
#         "8": 0,
#         "9": 0,
#         "10": 0,
#         "11": 0,
#         "12": 0
#     }

#     for el in range(NUMBER_ATTEMPTS + 1):
#         roll_one = dice_roll()
#         roll_two = dice_roll()
#         sum_roll = str(roll_one + roll_two)
#         # current = values.get(sum_roll)
#         # values.update({sum_roll: current + 1})
#         values[sum_roll] += 1
    
#     for k, v in values.items():
#         values[k] = round(v / NUMBER_ATTEMPTS * 100, 2)
    
#     return values

# def write_results(result):
#     with open("m08_02/data.md", "w") as f:
#         f.write('| Викид | Експеримент % | Орієнтир % |\n')
#         f.write('| :---- | :-----------: | :--------: |\n')
#         for k in expected_outcome.keys():
#             f.write("|{:<7}|{:^15}|{:^12}|\n".format(k, result.get(k), expected_outcome.get(k)))

# result = experiment()
# write_results(result)

from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN, ROUND_HALF_UP

# f = 0.2 + 0.1 + 0.3 - 0.5
# print(f)

# rf = D("0.2") + D("0.1") + D("0.3") - D("0.5")
# print(rf)

# not_precision = D("1") / D("3")
# print(not_precision)

# getcontext().prec = 6
# precision = D("1") / D("3")
# print(precision)
# precision2 = D("11") / D("3")
# print(precision2)

# Округлення чисел

"""
Відповідно до офіційної документаії Python, ось що робить кожен з цих режимів:

- ROUND_FLOOR: число округлюється до від'ємної нескінченності.
- ROUND_CEILING: число округлюється до нескінченності або додатньої нескінченності.
- ROUND_HALF_DOWN: числа округлюються до найближчого числа. Якщо є нічия, число округлюється до нуля. Є рівновіддалені числа, котрі можна округляти як в більшу, так і в меншу сторону. Наприклад, таке число, як 4,25, можна округлити як в сторону 4,2, так и 4,3.
- ROUND_HALF_UP: числа округлюються до найближчого числа. Якщо є нічия, число округлюється від нуля.
- ROUND_UP: число округлюється від нуля.
- ROUND_DOWN: число округлюється до нуля.
- ROUND_HALF_EVEN: числа округлюються до найближчого числа. Будь-які нічиї округлюються до найближчого парного цілого числа.
- ROUND_05UP: числа округлюються від нуля, якщо останнє число рівне 0 або 5. Якщо ні, то числа округлюються до нуля.

За замовчуванням округлення описується константою ROUND_HALF_EVEN
"""

# num = D("1.45")
# print(num.quantize(D("1.0"), rounding=ROUND_HALF_EVEN))
# print(num.quantize(D("1.0"), rounding=ROUND_HALF_UP))

# print(D("3.14159").quantize(D("1.000")))

# r_num = (D("11") / D("3")).quantize(D("1.000000"))
# print(r_num)

# f = D.from_float(1.37)
# s = D.from_float(1.5)

# print(f, s)

# f2 = D("1.37")
# s2 = D("1.5")
# print(f2, s2)

"""
Порівняння двох десяткових чисел
Значення 0 вказує, що обидва числа рівні,
значення 1 вказує, що перше число більше другого числа,
а значення -1 вказує, що перше число менше другого.
"""

# print(D("1.2").compare(D("1.1")))
# print(D('1.0').compare(D('1.1')))
# print(D('1.0').compare(D('1.0')))

# print(0.1 + 0.2 == 0.3)
# num1 = D("0.1") + D("0.2")
# num2 = D("0.3")
# print(num1.compare(num2))

# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------
# Нижче даю те, що не встигли опрацювати на занятті

# 1. Використання функцій з модулю math + знайомство з методом fabs (те саме, що і abs, тільки для float)

# import math

# x = float(input('x='))
# y = float(input('y='))

# log(y ** (-sqrt(|x|))) * (sin(x) + e ** (x + y))
# print(math.log(math.pow(y, -math.sqrt(math.fabs(x)))) * (math.sin(x) + math.exp(x + y)))
# a = math.log(math.pow(y, -math.sqrt(math.fabs(x)))) * \
#     (math.sin(x) + math.exp(x + y))

# print(a)

# 2. Функція math.isclose()
# import math

# print(0.1 + 0.2 == 0.3)
# r = math.isclose(0.1 + 0.2, 0.3)
# print(r)

# r = math.isclose(0.1, 0.10000000009)
# print(r)

# print(abs(0.1 - 0.1001) < 0.00001)
# r = math.isclose(0.1, 0.1001, abs_tol=0.00001)
# print(r)

# 3. 
"""
Іменовані кортежі
Клас collections.namedtuple дозволяє створити тип даних, що поводиться як кортеж з можливістю присвоїти кожному елементу ім'я, за яким надалі можна отримати доступ
"""

# import collections

# Point = collections.namedtuple('Point', ['x', 'y', 'z'])
# p = Point(1, 2, 3)
# print(p.x, p.y, p.z)

# Dog = collections.namedtuple('Dog', ['nickname', 'age', 'owner'])
# print(Dog.__name__)
# cat = Dog('Simon', 4, 'Krabat')
# print(type(cat))
# print(f'This is a cat {cat.nickname}, {cat.age} age, his owner is {cat.owner}')

# 4.
# from collections import namedtuple

# color_type = namedtuple('RGB', ['red', 'green', 'blue'])

# cat = color_type(100, 20, 34)
# rabbit = color_type(0, 234, 123)
# print(cat)

# 5.
"""
Counter
Наприклад є набір температур за перші 15 днів січня. Знайти кількість спільних температур, найчастішу
"""

# import collections

# temperatures = [0.5, 0.0, -3.5, 0.0, 2.5, 3.5, 4.0, 0.5, 3.5, 5.5, 6.0, 10.0, 12.5]

# t_count = collections.Counter(temperatures)
# print(t_count)
# print(t_count.most_common(1))
# print(t_count.most_common())

# 6.
# """
# Реалізувати функцію, що повертає n найчастіших і n найрідших чисел з файлу
# """

# from collections import Counter

# filename = 'm08_02/numbers.txt'


# def num_counter(filename, n):
#     with open(filename, 'r', encoding='utf-8') as file:
#         data = file.read()
#     counter = Counter([int(i) for i in data.split(',')])
#     print(counter)
#     ordered = counter.most_common(len(counter))
#     print(ordered)
#     return [i for i, _ in ordered[:n]], [i for i, _ in ordered[-n:]]


# result = num_counter(filename, 10)
# a, _ = (10, 5)
# print(a)
# print(_)
# print(result)

# 7.
"""
defaultdict
collections.defaultdict нічим не відрізняється від звичайного словника за винятком того, що за замовчуванням завжди викликається функція, що повертає значення:
"""
# from collections import defaultdict

# # { key: [], key2: []}
# data_d = defaultdict(list)
# # data_d[0] = []
# data_d[0].append(10)
# data_d[0].append(1)
# data_d[1].append(100)
# print(data_d)

# colors = [('yellow', 1), ('blue', 3), ('yellow', 5), ('blue', 10), ('red', 13)]
# colors_d = defaultdict(list)
# for k, v in colors:
#     colors_d[k].append(v)
# print(colors_d)


# colors = [('yellow', 1), ('blue', 3), ('yellow', 5), ('blue', 10), ('red', 13)]


# def my_dict():
#     return {}


# colors_d = defaultdict(my_dict)
# for k, v in colors:
#     colors_d[k].update({k + str(v): v})
# print(colors_d)


# temperatures = [0.5, 0.0, -3.5, 0.0, 2.5, 3.5, 4.0, 0.5, 3.5, 5.5, 6.0, 10.0, 12.5]


# def my_add():
#     return 5


# temperatures_d = defaultdict(my_add)
# for i, el in enumerate(temperatures):
#     temperatures_d[i] += el

# print(list(temperatures_d.values()))

# 8.
"""
defaultdict: Зручно якщо ми розбиваємо на різні списки набори телефонних операторів
"""

# from collections import defaultdict

# phone_numbers = ['0509993636', '0679993636', '0959993636',
#                  '0969993636', '0509993637', '0639993636', '0509993632', '0339993632']

# phone_operator_numbers = defaultdict(list)

# for ph in phone_numbers:
#     if ph.startswith('050') or ph.startswith('095'):
#         phone_operator_numbers['Vodafone'].append(ph)
#     elif ph.startswith('067') or ph.startswith('096'):
#         phone_operator_numbers['Kyivstar'].append(ph)
#     elif ph.startswith('063') or ph.startswith('093'):
#         phone_operator_numbers['Lifecell'].append(ph)
#     else:
#         phone_operator_numbers['Unknown'].append(ph)

# print(phone_operator_numbers)

# 9. 
"""
collections.deque(iterable, [maxlen]) - створює чергу з об'єкту, що ітерується, з максимальною довжиною maxlen. Черги дуже схожі на списки, за винятком того, що додавати і видаляти елементи можна або справа, або зліва.

Методи, визначені в deque:

append(x) - додає x в кінець.

appendleft(x) - додає x в початок.

clear() - очищує чергу.

count(x) - кількість елементів, що дорівнюють x.

extend(iterable) - додає в кінець всі елементи iterable.

extendleft(iterable) - додає в початок всі елементи iterable (починаючи з останнього елементу iterable).

pop() - видаляє і повертає останній елемент черги.

popleft() - видаляє і повертає перший елемент черги.

remove(value) - видаляє перше вхождення value.

reverse() - розвертає чергу.

rotate(n) - послідовно переносить n елементів з кінця в початок (якщо n від'ємне, то навпаки).
"""
# from collections import deque

# l = list(range(1, 10))
# l_deque = deque(l)
# print(l_deque)
# l_deque = deque(l, 5)
# print(l_deque)

# l_deque.appendleft(10)
# l_deque.append(11)
# print(l_deque)
# print(l_deque.count(10))
# print(l_deque.index(6))

# l_deque.rotate(2)
# print(l_deque)

# l_deque.reverse()
# print(l_deque)

# 10. 

# #  List Comprehension

# squares = []

# for i in range(20):
#     squares.append(i**2)

# print(squares)

# sq = [i**2 for i in range(20)]
# print(sq)

# 11. 
# # Dict Comprehension

# squares = {}

# for i in range(20):
#     squares[i] = i**2

# print(squares)

# sq = {i: i**2 for i in range(20)}
# print(sq)

# 12.
#  Set Comprehension
# squares = set()

# for i in range(20):
#     squares.add(i**2)

# print(squares)

# sq = {i**2 for i in range(20)}
# print(sq)

# 13.
# # List: Наприклад для температур треба врахувати похибку і підвищити кожну температуру на 0.5 градуса

# temps = [0.5, 0.0, -3.5, 0.0, 2.0, 3.5, 0.5,
#          -4.0, -3.5, -0.5, -3.5, -10.5, -14.0, -1.0, -1.0]

# fix_t = [t + 0.5 for t in temps]
# print(fix_t)

# # Set: для цього ж списку температур знайдемо унікальні значення

# unique_t = {t + 0.5 for t in temps}
# print(unique_t)

# # Dict: створимо словник відповідності старої і виправленої температури

# tr_t = {t: t + 0.5 for t in temps}
# print(tr_t)

# 14. Comprehension з вкладеними циклами for

# a = range(4)
# b = range(3)

# l = []

# for x in a:
#     for y in b:
#         l.append((x, y))
# print(l)

# l = [(x, y) for x in a for y in b]
# print(l)

# 15. Comprehension з умовою if

# x = range(10)

# l = []
# for el in x:
#     if el % 2:
#         l.append(el)
# print(l)
# l = [el for el in x if el % 2]
# print(l)