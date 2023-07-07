# double underscore = dunder
# магічні = dunder
# __init__(self, *args, **kwargs)
# __str__(self)
# __repr__(self)
# __getitem__(self, key)
# __setitem__(self, key, value)
# __call__(self, *args, **kwargs)
# __enter__(self)
# __exit__(self, exception_type, exception_value, traceback)
# __iter__(self)
# __next__(self)
# __add__(self, other)
# __sub__(self, other)
# __mul__(self, other)
# __div__(self, other)
# __pow__(self, other)
# __eq__(self, other)
# __ne__(self, other)
# __lt__(self, other)
# __gt__(self, other)
# __le__(self, other)
# __ge__(self, other)

class Journal:
    def __init__(self, students=None):
        self.students = students or {}
    
    def __getitem__(self, name):
        return self.students.get(name, 0)

    def __str__(self):
        return str(self.students)
    
    def __setitem__(self, name, grade):
        self.students[name] = grade

    def __call__(self):
        return f"This journal has these grades: {list(self.students.values())}"
    

journal = {
    "Name A": 90,
    "Name B": 55
}

b = Journal(journal)
# print(b.students["Name A"])
# print(b["Name A"])  # b.__getitem__("Name A")

b.students["Name C"] = 100
b["Name D"] = 5  # b.__setitem__("Name D", 5)
# print(b)

a = b()  # b.__call__
# print(a)


class Adder:
    def __init__(self, add_value):
        self.add_value = add_value

    def __call__(self, value):
        self.add_value = self.add_value + value
        return self.add_value


two_adder = Adder(2)
# print(two_adder(5))  # 7
# print(two_adder(4))  # 6

three_adder = Adder(3)
# print(three_adder(5))  # 8
# print(three_adder(4))  # 7


class Session:
    def __init__(self, addr, port=8080):
        self.addr = addr
        self.port = port

    def __enter__(self):
        self.connected = True
        print(f"connected to {self.addr}:{self.port}")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.connected = False
        if exception_type is not None:
            print("Some error!")
        else:
            print("No problem")

# session = Session("https://google.com")

# with session as f:
#     print(f.addr)
#     # raise ValueError("test value error")
#     print("fdsf")

# print(session.connected)

# with Session("goit.com") as second_session:
#     print("some work")

class Iterable:
    MAX_VALUE = 10
    def __init__(self):
        self.current_value = 0

    def __next__(self):
        if self.current_value < self.MAX_VALUE:
            self.current_value += 1
            return self.current_value
        raise StopIteration
    
    def __iter__(self):
        return self


# class CustomIterator:
#     def __iter__(self):
#         return Iterable()


c = Iterable()
# for i in c:
#     print(i)



# access modifiers
# public -> доступні всім і будь-де
# protected -> _... доступні і до змін всюди, але створений для себе чи дочірніх класів
# private -> __... тільки в самому класі

class Secret:
    public_field = 'this is public'
    _private_field = 'avoid using this please'
    __real_secret = 'I am hidden'

    @property
    def real_secret(self):
        # authorization
        return self.__real_secret
    
    @real_secret.setter
    def real_secret(self, value):
        self.__real_secret = value

s = Secret()
print(s.public_field)           # this is public
print(s._private_field)         # avoid using this please
# print(s.__real_secret)
print(s._Secret__real_secret)   # I am hidden
print(s.real_secret)
s.real_secret = 10
print(s.real_secret)
# s.public_field = "error"

# @property

class PositiveNumber:
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if new_value > 0:
            self.__value = new_value
        else:
            print('Only numbers greater than zero are accepted')


p = PositiveNumber()
p.value = 1
print(p.value)  # 1
p.value = -1    # Only numbers greater zero accepted
p._PositiveNumber__value = -1
print(p.value)  # -1s


class CreditCard:
    def __init__(self, balance):
        self.__balance = balance
    
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, new_balance):
        self.__balance = new_balance

    def __str__(self):
        return f"Credit card with {self.balance} on it"
    
    def __add__(self, other):
        if isinstance(other, CreditCard):
            return CreditCard(self.balance + other.balance)
        else:
            return CreditCard(self.balance + other)
    
    def __sub__(self, other):
        return CreditCard(self.balance - other.balance)
    
    def __eq__(self, other):
        return self.balance == other.balance
    
    def __gt__(self, other):
        if isinstance(other, CreditCard):
            return self.balance > other.balance
        else:
            return self.balance > other

a = CreditCard(100)
b = CreditCard(200)

print(a)
print(b)

c = a + b  # a.__add__(b)
print(c)
print(a-b)

print(a+b-c)  # (a.__add__(b).__sub__(c))
print(a+100)  # a.__add__(100)
d = CreditCard(100)
print(a == d)  # a.__eq__(d)
print(a > d)  # a.__gt__(d)
print(a > 0)  # a.__gt__(0)

from collections import UserDict

class MyDict(UserDict):
    def __add__(self, other):
        self.data.update(other)
        return self

    def __sub__(self, other):
        for key in other:
            if key in self.data:
                self.data.pop(key)
        return self


d1 = MyDict({1: 'a', 2: 'b'})
d2 = MyDict({3: 'c', 4: 'd'})

d3 = d1 + d2  # d1.__add__(d2)
# print(d3)   # {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

d4 = d3 - d2
# print(d4)   # {1: 'a', 2: 'b'}

