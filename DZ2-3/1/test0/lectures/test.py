import csv
import json
import pickle
import copy
from collections import UserList
from datetime import datetime
from time import sleep

# with open("names.csv", "w") as f:
#     fields_name = ["first_name", "last_name"]
#     writer  = csv.DictWriter(f, fieldnames=fields_name)
#     writer.writeheader()
#     writer.writerow({
#         "first_name": "First Name 1",
#         "last_name": "Last Name 1"
#     })
#     writer.writerow({
#         "first_name": "First Name 2",
#         "last_name": "Last Name 2"
#     })

# with open("names.csv") as f:
#     print(f.read())

# users = [
#     {"name": "Микола", "age": 22, "sex": "male"},
#     {"name": "Марія", "age": 20, "sex": "female"},
#     {"name": "Назар", "age": 25, "sex": "male"}
# ]

# with open("users.csv", "w") as f:
#     columns = users[0].keys()
#     writer = csv.DictWriter(f, fieldnames=columns)
#     writer.writeheader()
#     # for row in users:
#     #     writer.writerow(row)
#     writer.writerows(users)

# with open("users.csv") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         print(row)

# country_codes = {}

# with open("m12_01/csv/countries.csv") as f:
#     reader = csv.reader(f)
#     header = next(reader)
#     print(header)
#     for line in reader:
#         country_codes[line[0]] = line[1]

# # print(country_codes)
# print(country_codes["UA"])

# with open("table.csv", "w") as f:
#     writer = csv.writer(f)
#     for i in range(1, 21):
#         writer.writerow([i**2, i**3])

# with open("table.csv") as f:
#     reader = csv.reader(f)
#     res = []
#     for line in reader:
#         res.append(line)

# print(res)

# d = {"a": 1}
# l = [1, 2.2]
# t = (3, 4)
# s = "I am string!"
# b = True
# st = {1, 2, "Test"}
# obj = {
#     "tuple": t,
#     "list": l,
#     "dict": d,
#     "string": s,
#     "bool": b
# }

# print(json.dumps(d))
# print(json.dumps(l))
# print(json.dumps(t))
# print(json.dumps(s))
# print(json.dumps(b))
# # print(json.dumps(st))

# with open("storage.json", "w") as f:
#     json.dump(obj, f, indent=4)

# with open("storage.json") as f:
#     store = json.load(f)

# print(store)
# print(store.get("dict").get("a"))

# data = {
#     "developer": {
#         "name": "Ілля",
#         "job": "програміст"
#     }
# }

# with open("data_user.json", "w") as f:
#     json.dump(data, f, indent=6, ensure_ascii=False)

# with open("data_user.json") as f:
#     print(json.load(f))

# d = {"some key": 12445}

# with open("my_data.bin", "wb") as f:
#     pickle.dump(d, f)

# d_bytes = pickle.dumps(d)
# print(d_bytes)

# with open("my_data.bin", "rb") as f:
#     db = pickle.load(f)

# print(db)
# print(pickle.loads(d_bytes))

# users = [
#     ["Tom", 28, True],
#     ["Alice", 23, False],
#     ["Bob", 34, False]
# ]

# with open("user.dat", "wb") as f:
#     pickle.dump(users, f)

# with open("user.dat", "rb") as f:
#     users_from_file = pickle.load(f)
#     print(users_from_file)


# class A:
#     x = "some"

#     def __init__(self):
#         print("new A object!")
#         self.y = "Інша змінна"

#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y

# a = A()
# ser = pickle.dumps(a)

# print(ser)
# restored_a = pickle.loads(ser)
# print(restored_a.y)
# print(a, restored_a)
# print(a == restored_a)

# ser_class = pickle.dumps(A)
# A.x = 5
# restored_A = pickle.loads(ser_class)
# print(restored_A.x)
# print(A, restored_A)
# print(A == restored_A)
# print(int == int)

# with open("m12_02/test2.py") as f:
#     pickled_code = pickle.dumps(f.read())
#     print(pickled_code)

# with open("m12_02/test3.py", "w") as f:
#     f.write(pickle.loads(pickled_code))

"""
Інтерпретатор Python лінивий і якщо його явно не попросити створити копію об'єкту, він створить новий вказівник на все той самий об'єкт. Не завжди така поведінка вітається. Для того щоб створити копію об'єкту в пакеті copy є функції:
- copy -- поверхнева копія
- deepcopy -- глибока копія.
"""

# l = [1, 2, 3, ["a", "b", "c"]]

# l1 = l
# l2 = l.copy()
# l3 = l[:]
# l_copy = copy.copy(l)
# l_deepcopy = copy.deepcopy(l)

# print(l1 == l, l1 is l)
# print(l2 == l, l2 is l)
# print(l3 == l, l3 is l)
# print(l_copy == l, l_copy is l)
# print(l_deepcopy == l, l_deepcopy is l)

# # print(l_copy[3] is l[3])

# l[0] = 9
# print(l, l_copy, l_deepcopy)
# l[3][0] = "D"
# print(l, l_copy, l_deepcopy)

# Під капотом функції copy, deepcopy викликають методи __copy__, __deepcopy__.

# class CopyList(UserList):
#     def __init__(self, *data):
#         super().__init__()
#         self.data = list(data)
    
#     def __copy__(self):
#         n = CopyList()
#         n.data = self.data
#         return n

#     def __deepcopy__(self, memo):
#         n = CopyList()
#         memo[id(self)] = n
#         for el in self.data:
#             n.append(copy.deepcopy(el, memo))
#         # Словник memo зберігає в якості ключів id об'єктів і самі об'єкти як значення, щоб не було рекурсії при копіюванні
#         return n


# a = CopyList(1,2,3)
# copy_list = CopyList([1,2,3,4])
# print(a.data, copy_list.data)

# copy_list_copy = copy.copy(copy_list)
# copy_list_deepcopy = copy.deepcopy(copy_list)

# print(copy_list_copy, copy_list_deepcopy)

# print(id(copy_list), copy_list)
# print(id(copy_list_copy), copy_list_copy)
# print(id(copy_list_deepcopy), copy_list_deepcopy)

# print(id(copy_list[0]), copy_list[0])
# print(id(copy_list_copy[0]), copy_list_copy[0])
# print(id(copy_list_deepcopy[0]), copy_list_deepcopy[0])

# Реалізувати pickable клас, що зберігає дату і час коли об'єкт цього класу серіалізували і
# коли розпакували.

# class RememberAll:
#     def __init__(self, *args):
#         self.data = list(args)
#         self.saved = None
#         self.restored = None
    
#     def __getstate__(self):
#         state = self.__dict__.copy()
#         state["saved"] = datetime.now()
#         return state
    
#     def __setstate__(self, state):
#         # self.__dict__ = state
#         self.__dict__.update(state)
#         self.restored = datetime.now()

# r = RememberAll(1,2,3,4,5)
# print(r.data)
# r_dump = pickle.dumps(r)
# print(r_dump)
# sleep(1)
# r_load = pickle.loads(r_dump)
# print(r_load.data)
# print(r_load.saved, r_load.restored)
# print(r.saved, r.restored)

# Друк і нумерація рядків в текстовому файлі.

# class SongReader:
#     def __init__(self, filename):
#         self.filename = filename
#         self.file = open(self.filename)
#         self.line_count = 0
    
#     def readline(self):
#         self.line_count += 1
#         line = self.file.readline()
#         if not line:
#             return
#         if line.endswith("\n"):
#             line = line[:-1]
#         return f"{self.line_count}: {line}"
    
#     def __getstate__(self):
#         state = self.__dict__.copy()
#         # state["file"] = None
#         del state["file"]
#         return state
    
#     def __setstate__(self, state):
#         self.__dict__.update(state)
#         file = open(self.filename)
#         for _ in range(self.line_count):
#             file.readline()
#         self.file = file
    

# reader = SongReader("m12_02/order/song.txt")
# print(reader.readline())
# print(reader.readline())
# print(reader.readline())
# new_reader = pickle.loads(pickle.dumps(reader))
# while True:
#     line = new_reader.readline()
#     if not line:
#         break
#     print(line)

# print("----------------------")
# print(reader.readline())