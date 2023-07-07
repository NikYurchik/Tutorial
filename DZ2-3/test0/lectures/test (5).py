# from datetime import datetime


# test_str = "21/03/1978"

# expected_strs = "1978/03/21", "03/21/1978"

# def change_date_format(str_datetime):
#     dt = datetime.strptime(str_datetime, "%d/%m/%Y")
#     first_str = dt.strftime("%Y/%m/%d")
#     second_str = dt.strftime("%m/%d/%Y")
#     return first_str, second_str


# result = change_date_format(test_str)
# print(result)
# print(result == expected_strs)

# test_list_str = [
#     "21/03/1978",
#     "12/05/1989",
#     "24/05/2023",
#     "02/10/1950",
#     "19/01/1012"
# ]

# updated_list_comprehension = [change_date_format(x) for x in test_list_str]
# updated_list = []
# for x in test_list_str:
#     res = change_date_format(x)
#     updated_list.append(res)
# print(updated_list)
# print(updated_list == updated_list_comprehension)

from collections import defaultdict
# dd = defaultdict(list)
# dd['key'].append(1)
# print(dd)

# dd['key'].append(2)
# print(dd)

# dd['key'].append(3)
# print(dd)

# dep = [('Sales', 'John Doe'),
#        ('Sales', 'Martin Smith'),
#        ('Accounting', 'Jane Doe'),
#        ('Marketing', 'Elizabeth Smith'),
#        ('Marketing', 'Adam Doe')]

# dep_dd = {}
# for dep, person in dep:
#     if dep not in dep_dd:
#         dep_dd[dep] = []
#     dep_dd[dep].append(person)


# dep_dd = defaultdict(list)
# for department, employee in dep:
#     dep_dd[department].append(employee)

# print(dep_dd["Sales"][0])

# dep = [('Sales', 'John Doe'),
#        ('Sales', 'Martin Smith'),
#        ('Accounting', 'Jane Doe'),
#        ('Marketing', 'Elizabeth Smith'),
#        ('Marketing', 'Elizabeth Smith'),
#        ('Marketing', 'Adam Doe'),
#        ('Marketing', 'Adam Doe'),
#        ('Marketing', 'Adam Doe')]

# dep_dd = defaultdict(set)
# for department, employee in dep:
#     dep_dd[department].add(employee)

# dep = [('Sales', 'John Doe'),
#        ('Sales', 'Martin Smith'),
#        ('Accounting', 'Jane Doe'),
#        ('Marketing', 'Elizabeth Smith'),
#        ('Marketing', 'Adam Doe')]
# dd = defaultdict(int)
# for department, _ in dep:
#     dd[department] += 1
# print(dd)

# from collections import defaultdict
# s = 'mississippi'
# dd = defaultdict(int)
# for letter in s:
#     dd[letter] += 1

# print(dd)

# a = []
# b = set()

# a.append(2)
# a.append(2)
# print(a)
# b.add(2)
# b.add(2)
# print(b)

# from collections import Counter
# counter = Counter('mississippi')
# print(counter)

# from collections import defaultdict

# incomes = [('Books', 1250.25),
#            ('Books', 1300.6),
#            ('Books', 1420.00),
#            ('Tutorials', 560.00),
#            ('Tutorials', 630.00),
#            ('Tutorials', 750.00),
#            ('Courses', 2500.00),
#            ('Courses', 2430.00),
#            ('Courses', 2750.00),]


# dd = defaultdict(float)

# for product, income in incomes:

#     dd[product] += income


# for product, income in dd.items():

#     print(f'Total income for {product}: ${income:,.2f}')


# from collections import defaultdict

# def return_default():
#     default_value = "Not in dict"
#     return default_value


# dd = defaultdict(return_default)

# for i in range(10):
#     dd[i] = i ** 2

# print(dd[20])
# print(dd)

# from collections import Counter

# l = [i for i in range(7)]
# l.extend([i for i in range(4,8)])
# l.extend([True for _ in range(5)])
# print(l)
# c = Counter(l)
# print(c)
# print(c.most_common(1))

# def decode(data):
#     if data:
#         if len(data) == 2:
#             res = []
#             for i in range(data[1]):
#                 res.append(data[0])
#             return res
#         else:
#             return decode(data[:2]) + decode(data[2:])
#     else:
#         return []
    
# print(decode(["X", 3, "Z", 2, "X", 2, "Y", 3, "Z", 2]))

# def encode(data):
#     if not data:
#         return []
#     counter = 0
#     res = []
#     for ind, i in enumerate(data):
#         if not res:
#             res.append(i)
#             counter += 1
#         elif i == res[-1]:
#             counter += 1
#         else:
#             res.append(counter)
#             res.extend(encode(data[ind:]))
#             return res
#     res.append(counter)
#     return res

# def encode(data):
#     if not data:
#         return []
#     stack =[]
#     for el in data:
#         if not stack:
#             stack.append(el)
#         elif el == stack[-1]:
#             stack.append(el)
#         else:
#             return [stack[-1], len(stack)] + encode(data[len(stack):])
#     return [stack[-1], len(stack)] 

# def encode(data): 
#     if len(data) == 0: 
#         return [] 
#     char = data[0] 
#     counter = 1 
#     while counter < len(data) and data[counter] == char: 
#         counter += 1 
#     return [char, counter] + encode(data[counter:]) 

# def encode(data): 
#     if not data: 
#         return [] 
#     def encode_recursive(data, count): 
#         if len(data) == 1: 
#             return [data[0], count] 
#         if data[0] == data[1]: 
#             return encode_recursive(data[1:], count + 1) 
#         else: 
#             return [data[0], count] + encode_recursive(data[1:], 1) 
#     return encode_recursive(data, 1)

# def encode(data):
#     if not data:
#         return []
#     result = []
#     count = 1
#     current = data[0]
    
#     for i in range(1, len(data)):
#         if data[i] == current:
#             count += 1
#         else:
#             result.append(current)
#             result.append(count)
#             current = data[i]
#             count = 1
#     result.append(current)
#     result.append(count)
#     # print(result)
    
#     return result

# print(encode("XXXZZXXYYYZZ"))

# from collections import namedtuple

# Person = namedtuple("Person", ("name", "surname", "age"))

# p = Person("name1", "surname1", 18)

# print(p)  # Person(name='name1', surname='surname1', age=18)
# print(p._fields)  # ('name', 'surname', 'age')
# print(p._asdict())  # {'name': 'name1', 'surname': 'surname1', 'age': 18}

# from datetime import datetime

# dt = datetime.now()
# print(dt)
# print(type(dt))

# ts = dt.timestamp()
# print(ts)
# print(type(ts))

# import random

# def get_numbers_ticket(min, max, quantity):
#     res = []
#     new_list = list(range(min,max))
#     if min < quantity or quantity < max:
#         x = random.sample(new_list, quantity)
#         f = res.extend(x)
#         return f
#     else:
#         return []

# w = get_numbers_ticket(0, 100, 5)
# print(w)

# import random

# def get_numbers_ticket(min, max, quantity):
#     res = []
#     new_list = list(range(min,max))
#     if min < quantity or quantity < max:
#         x = random.sample(new_list, quantity)
#         res.extend(x)
#         return res
#     else:
#         return []

# w = get_numbers_ticket(0, 100, 5)
# print(w)

# from datetime import datetime

# s = "2021-05-27 17:08:34.149TEST"

# print(datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%fTEST"))

# dt = datetime.now()

# print(dt.strftime("abcd%Yefgh%mOOO"))

# from clean_folder.clean_folder import *

# print(CYRILLIC_SYMBOLS)

# from collections import defaultdict
# map = defaultdict(dict)
# # map["type"] = {}
# map = {
#     "type": {
#         "1": "Gems",
#         "2": "Coins",
#         "3": "Energy",
#         "4": "EnergyMax",
#         "5": "Story",
#         "6": "Hints",
#         "7": "Bundle",
#         "10": "EnergyForAds",
#     },
#     "subType": {
#         "0": "None",
#         "1": "Magnifier",
#         "2": "Reagent",
#         "3": "Foto",
#     },
#     "appearanceType": {
#         "0": '{"Regular":""}',
#         "1": '{"LevelRequired":"4"}',
#     },
#     "label": {
#         "None": "",
#     },
#     "title": {
#         "None": "",
#         "Starter": "bank_starter",
#         "Energy Pack": "bank_energy_pack",
#         "Best Deal": "bank_best_deal",
#         "Super Deal": "bank_super_deal",
#     },
# }

# def normalize(key):
#     return map[key]
    
# print(normalize("test"))
# print(map.get(key).get(str(item), str(item)))


# Чи можна такий вираз зпростити за допомогою defaultdict? Маю на увазі доступ до values
#  return self.map.get(key).get(str(item), str(item))
# Чи немає смислю використовувати тут defaultdict?
