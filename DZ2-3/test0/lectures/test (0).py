"""
Протокол ітератора (iterable) в Python реалізований за допомогою методу __iter__. 
Цей метод має вертати ітератор (iterator).
Ітератором може бути будь-який об'єкт, в якого є метод __next__, що при кожному виклику 
повертає значення.
Щоб створити ітератор (iterator), достатньо реалізувати метод __next__.
"""

from random import randint

class RandIterator:
    def __init__(self, start, end, quantity):
        self.start = start
        self.end = end
        self.quantity = quantity
        self.count = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        self.count += 1
        if self.count > self.quantity:
            raise StopIteration
        else:
            return randint(self.start, self.end)
        

# for rn in RandIterator(1, 20, 5):
#     print(rn)

"""
Реалізуємо ітератор, що виконує ітерацію задану кількість разів по заданій послідовності
"""

class MyIterator:
    def __init__(self, seq, count_loop):  
        self.seq = seq
        self.count_loop = count_loop
        self.loop = 0
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.loop >= self.count_loop:
            raise StopIteration
        else:
            value = self.seq[self.index]
            self.index += 1
            if self.index == len(self.seq):
                self.index = 0
                self.loop += 1
            return value


seq = ["a", "b", "c"]
# for el in MyIterator(seq, 2):
#     print(el)

# Методи __repr__ и __str__


class Car:
    store_name = "Мій магазин машин"

    def __init__(self, year, mark, model, color):
        self.year = year
        self.mark = mark
        self.model = model
        self.color = color
    
    def __repr__(self):
        return f"Car({self.year}, '{self.mark}', '{self.model}', {self.color})"
    
    def __str__(self):
        return f"{self.store_name} - {self.mark}.{self.model}: {self.year}, {self.color}"
    

car = Car(2016, "Mazda", "Model Y", "White")
# print(car)
# print(repr(car))
# list_of_cars = [car]
# print(list_of_cars)
# for car in list_of_cars:
#     print(car)


# Методи __getitem__ и __setitem__
from collections import UserList

class PositiveNumbers(UserList):
    def __init__(self, data=None):
        data = data or []
        super().__init__()
        # self.data = [el for el in list(filter(lambda x: x > 0), data)]
        self.data = [el for el in data if el > 0]

    def __setitem__(self, index, value):
        if value > 0 and index < len(self.data):
            self.data[index] = value

    def __getitem__(self, index):
        return self.data[index] 
    
    def append(self, item):
        if item > 0:
            super().append(item)



# nums = PositiveNumbers([2, -4, 5])
# print(nums)
# nums[1] = -6
# print(nums)
# nums.append(55)
# nums.append(-9)
# nums.append(1)
# print(nums[2])

# Функтор

class Count:
    def __init__(self, init_steps=0):
        self.steps = init_steps

    def __call__(self, new_steps):
        self.steps += new_steps


# count_step = Count(100)
# print(count_step.steps)
# # count_step.steps += 20
# count_step(20)
# count_step(50)
# print(count_step.steps)

"""
Для того, щоб об'єкт можна було використати в конструкції with ... as ...: в об'єкті мають бути 
визначені два методи: __enter__, __exit__.

__enter__ -- метод, що приймає тільки один аргумент self. Якщо метод щось вертає, то його вивід 
буде записаний в змінну val в конструкції with context_manager as val:.

__exit__ -- обов'язково приймає 4 аргументи: self, exception type, exception value, 
exception traceback.
Ці аргументи треба для коректної обробки винятків всередині __exit__.
"""

class FileWrite:
    def __init__(self, filename):
        self.file = None
        self.opened = False
        self.filename =filename

    def __enter__(self):
        self.file = open(self.filename, "w")
        self.opened = True
        return self.file
    
    def __exit__(self, exc_type, exc_value, tb):
        print(exc_type, exc_value, tb)
        if self.opened:
            self.file.close()
        self.opened = False

# with FileWrite("new_file.txt") as f:
    # raise ValueError("test value error")
    # f.write("Hello world!")

# print("end")

# Написати Contex Manager FileReader, що пише в лог timestamp коли файл був відкритий,
# timestamp коли файл був закритий, ім'я файлу, і як довго файл був відкритий з точністю до секунд.

from datetime import datetime
from time import sleep

class FileReader:
    def __init__(self, filename):
        self.file = None
        self.opened = False
        self.filename = filename
        self.log = ""
        self.timestamp = None
    
    def __enter__(self):
        self.file = open(self.filename)
        self.opened = True
        self.timestamp = datetime.now().timestamp()
        msg = "|{:<20}|{:^15}| open\n".format(self.timestamp, self.filename)
        self.log += msg
        return self.file
    
    def __exit__(self, exc_type, exc_value, tb):
        if self.opened:
            self.file.close()
            timestamp = datetime.now().timestamp()
            diff = timestamp - self.timestamp
            msg = "|{:<20}|{:^15}| closed {:>15} s\n".format(timestamp, self.filename, round(diff, 6))
            self.log += msg
            self.opened = False


reader = FileReader("new_file.txt")
# with reader as f:
#     # sleep(2)
#     print(f.read())


# with reader as f:
#     # sleep(1)
#     print(f.read())


# print(reader.log)

# Інкапсуляція в Python (property, setter)
class Animal:
    def __init__(self, nickname, age, weight):
        self.__nickname = None
        self.__age = None
        self.__weight = None
        # setters
        self.name = nickname
        self.age = age
        self.weight = weight
    
    @property
    def name(self):
        return self.__nickname

    @name.setter
    def name(self, nickname):
        if nickname:
            self.__nickname = nickname
        else:
            raise ValueError("Animals must have names!")
    
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, age):
        if 0 < age < 50:
            self.__age = age
        else:
            raise ValueError("Animals don't live that long!")
    
    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, weight):
        if weight > 0:
            self.__weight = weight
        else:
            raise ValueError("Animals must have some weight!")
    
chup = Animal("Chupakabra", 12, 100)
# print(chup.name, chup.age, chup.weight)

# try:
#     second_chup = Animal("Chupakabra", -3, 100)
# except ValueError as e:
#     print(e)

# Сховище з паролем
class KeyStore:
    def __init__(self, name, password):
        self.__password = None
        self.__name = None
        self.__secret = None
        self.name = name
        self.password = password

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def password(self):
        return "No access to the password!"
    
    @password.setter
    def password(self, password):
        if not self.__password:
            self.__password = password
        else:
            if self.is_validate():
                self.__password = password

    
    def is_validate(self):
        p = input("Enter password: ")
        if self.__password == p:
            print("OK")
            return True
        print("Wrong password")
        return False
    
    @property
    def secret(self):
        if self.is_validate():
            return self.__secret
        
    @secret.setter
    def secret(self, secret):
        if self.is_validate():
            self.__secret = secret


k_store = KeyStore("Illia", "123456")

# print(k_store.password)
# k_store.password = "567234"
# k_store.secret = "test"
# print(k_store.secret)

"""
Написати клас Adder, що реалізує метод add(self, y), і виводить повідомлення «Не реалізовано». 
Потім визначте два підкласи Adder, що реалізують метод додавання:

а) ListAdder з методом додавання, що повертає конкатенацію двох своїх аргументів (списків)

б) DictAdder з методом додавання, що повертає новий словник з елементами з двох словників
"""

class Adder:
    def __add__(self, obj):
        raise NotImplemented
    
class ListAdder(Adder):
    def __init__(self, value):
        self.value = value

    def __add__(self, obj):
        return self.value + obj.value
    

class DictAdder(Adder):
    def __init__(self, value):
        self.value = value
    
    def __add__(self, obj):
        return {**self.value, **obj.value}
    

# l1 = ListAdder([1, 2])
# l2 = ListAdder([3,4])
# l3 = l1 + l2
# print(l3, type(l3))

# d1 = DictAdder({"Volodymyr": 10, "Serhii": 12})
# d2 = DictAdder({"Roman": 15, "Kateryna": 7})

# d3 = d1+ d2
# print(d3, type(d3))

# Логічні операції

class Car:
    store_name = "Мій магазин машин"

    def __init__(self, year, mark, model, color, price):
        self.year = year
        self.mark = mark
        self.model = model
        self.color = color
        self.price = price
    
    def __repr__(self):
        return f"Car({self.year}, '{self.mark}', '{self.model}', {self.color})"
    
    def __str__(self):
        return f"{self.store_name} - {self.mark}.{self.model}: {self.year}, {self.color}"
    
    def __eq__(self, other):
        return self.price == other.price
    
    def __ne__(self, other):
        return self.price != other.price
    
    def __lt__(self, other):
        return self.price < other.price
    
    def __gt__(self, other):
        return self.price > other.price
    
    def __le__(self, other):
        return self.price <= other.price
    
    def __ge__(self, other):
        return self.price >= other.price


c1 =Car(2016, "Mazda", "Y", "White", 5500)
c2 = Car(2017, "Tesla", "X", "Black", 6500)

print(c1 > c2)


# ----------------------------------------------------------------------------------------

# Декоратори класів

def method_decorator(func):
    def wrapper(self, *args):
        print('---Decorator run--')
        result = func(self, *args)
        print('---Decorator end--')
        return result
    return wrapper


def class_decorator(cls):
    print('---Decorator class---')
    new_cls = cls
    new_cls.value = 42
    return new_cls


@class_decorator
class TestClass:
    name = 'TestClass'

    @method_decorator
    def info(self, user):
        return f'Hello {user}. This is {self.name}'


t = TestClass()
print(t.info('Oleksandr'))
print(t.value)
t.test = 10
print(t.test)


# __rmul__
"""
Реалізувати клас-список (list) в якому множення перевизначено як скалярний добуток векторів
"""

from collections import UserList


class MulArray(UserList):
    def __init__(self, *args):
        self.data = list(args)

    def __mul__(self, other):
        res = 0
        for i in range(min(len(self.data), len(other))):
            res += self.data[i] * other[i]
        return res

    def __rmul__(self, other):
        res = 0
        for i in range(min(len(self.data), len(other))):
            res += self.data[i] * other[i]
        return res


vec1 = MulArray(1, 2, 3)
vec2 = MulArray(3, 4, 5)

print(vec1 * vec2)
print(vec1 * [3, 3, 3])
print(vec2 * [1, 1, 1])
print([1, 1, 1] * vec2)