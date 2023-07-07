class User:
    def __init__(self, my_name, my_age):
        self.name = my_name
        self.age = my_age

    def hello(self):
        print(self.name, self.age)

    def set_age(self, new_age):
        self.age = new_age


class AdminUser(User):
    def __init__(self, admin_name, admin_age):
        super().__init__(admin_name, admin_age)
        self.admin_status = True

a = User("Name A", 99)
# a.hello()
# a.set_age(21)
# a.hello()

b = User("Name B", 100)
# b.hello()

c = AdminUser("test admin user", 9999)
# print(c.admin_status)
# c.hello()




class Human:
    def __init__(self, name):
        self.name = name
    def voice(self):
        print(f"Hello! My name is {self.name}")


class Developer(Human):
    def __init__(self, name, field_description, language):
        super().__init__(name)
        self.field_description = field_description
        self.language = language
    def make_some_code(self):
        return f"{self.field_description} is {self.value}"


class PythonDeveloper(Developer):
    def __init__(self, name, field_description, language):
        super().__init__(name, field_description, language)
        self.value = "Python"
    def print_value(self):
        print(self.value)


# class JSDeveloper(Developer):
#     value = "JavaScript"


p_dev = PythonDeveloper("Bob", "Bob as Python developer", "Python")
# p_dev.voice()   # Hello! My name is Bob
# print(p_dev.make_some_code())  # My Programming language is Python
# p_dev.print_value()

# js_dev = JSDeveloper()
# js_dev.make_some_code()  # My Programming language is JavaScript

class A:
    x = 'I am A class'


class B:
    x = 'I am B class'
    y = 'I exist only in B'


class C(A, B):
    z = "This exists only in C"

# class C(B, A):
#     z = "This exists only in C"

# c = C()
# MRO
# print(C.mro())
# print(c.z)  # This exists only in C
# print(c.y)  # I exist only in B
# print(c.x)  # I am A class

class D(C, B):  # те саме, що і D(C)
# class D(B, C):
    d_var = "ddddd"

# print(D.mro())

from collections import UserList, UserDict, UserString

# .data

from collections import UserDict


class ValueSearchableDict(UserDict):
    def has_in_values(self, value):
        return value in self.data.values()


as_dict = ValueSearchableDict()
as_dict['a'] = 1
# print(as_dict)
as_dict.has_in_values(1)    # True
as_dict.has_in_values(2)    # False

from collections import UserList

class CountableList(UserList):
    def sum(self):
        return sum(map(int, self.data))


countable = CountableList([1, '2', 3, '4'])
countable.append('5')
# print(countable)
# print(countable.sum())     # 15

from collections import UserString


class TruncatedString(UserString):
    MAX_LEN = 7
    def truncate(self):
        self.data = self.data[:self.MAX_LEN]


ts = TruncatedString('abcdefghjklmnop')
# print(ts)
ts.truncate()
# print(ts)   # abcdefg




def input_number():
    while True:
        try:
            num = input("Enter integer number: ")
            return int(num)
        except ValueError as e:
            print(e)
            print(f'"{num}" is not a number. Try again')


# num = input_number()
# print(ValueError.mro())



import string


class NameTooShortError(Exception):
    pass


class NameStartsFromLowError(Exception):
    pass


def enter_name():
    name = input("Enter name: ")
    if len(name) < 3:
        raise NameTooShortError
    if name[0] not in string.ascii_uppercase:
        raise NameStartsFromLowError



# while True:
#     try:
#         name = enter_name()
#         break
#     except NameTooShortError:
#         print('Name is too short, need more than 3 symbols. Try again.')
#     except NameStartsFromLowError:
#         print('Name should start from capital letter. Try again.')


class Mammal:
    phrase = ""
    def voice(self):
        return self.phrase
    

class Dog(Mammal):
    phrase = "Bark!"


class Cat(Mammal):
    phrase = "Meow!"


class Kitten(Cat):
    def voice(self):  # поліморфізм, тому що Kitten -> Cat -> Mammal (що вже містить voice())
        return f"Kitten says: {super().voice()}"


class Chupakabra:
    def voice(self):  # duck typing, тому що Chupakabra не наслідує Mammal, але створюємо метод voice ідентичний до Mammal.voice()
        return "Chupakabra voice!"


class Recorder:
    def record_animal(self, animal):
        voice = animal.voice()
        print(voice)


cat = Cat()
dog = Dog()
kitten = Kitten()
chu = Chupakabra()

r = Recorder()

# for animal in (cat, chu, dog, kitten):
#     r.record_animal(animal)

# print(cat.voice())
# print(dog.voice())
# print(kitten.voice())
# print(chu.voice())

