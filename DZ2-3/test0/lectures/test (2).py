"""
Базові принципи ООП - Інкапсуляція 

Об'єднання в одне ціле даних і алгоритмів обробки цих даних. В рамках ООП дані називаються полями об'єкту, а функції - об'єктними методами.
"""

# class Animal:
#     pet_pet = "test"
#     def __init__(self, nickname, age):
#         self.nickname = nickname
#         self.__pet_age = age
    
#     def get_info(self):
#         return f"It's an animal. Their name is {self.nickname} and they're {self.__pet_age} years old!"
    
#     def get_age(self):
#         return self.__pet_age

# cat = Animal("Cat nick", 7)
# dog = Animal("Dog nick", 6)
# print(cat.get_info())
# print(dog.get_info())
# print(Animal.pet_pet)

"""
Базові принципи ООП - Наслідування 

Наслідування це властивість об'єктів мати своїх нащадків. Об'єкт-нащадок автоматично наслідує від батька всі поля і методи, може доповнювати об'єкти новими полями і замінити (перекривати) методи батька або доповнювати їх.
"""

# class Animal:
#     def __init__(self, nickname, age):
#         self.nickname = nickname
#         self.age = age
    
#     def get_info(self):
#         return f"It's an animal. Their name is {self.nickname} and they're {self.age} years old!"
    
#     def get_age(self):
#         return self.age
    
#     def set_age(self, age):
#         self.age = age
    
# class Cat(Animal):
#     name = ["Cat"]

#     def __init__(self, nickname, age, owner):
#         super().__init__(nickname, age)
#         self.owner = owner

#     def sound(self):
#         return f"{self.nickname} says Meow!"

# cat = Cat("Simon", 4, "Yurii")
# print(cat.nickname)
# cat.age = 5
# print(cat.get_info())
# print(cat.sound())

# cat2 = Cat("Boris", 10, "Serhii")
# cat2.name[0] = "Boris Animal"
# print(Cat.name)
# print(dir(cat))

"""
Базові принципи ООП - Поліморфізм 

Поліморфізм - це властивість споріднених об'єктів (об'єктів, що мають одного спільного батька) вирішувати схожі за сенсом проблеми різними способами.
"""

# class Animal:
#     def __init__(self, nickname, age):
#         self.nickname = nickname
#         self.age = age

#     def get_info(self):
#         return f"It's animal. His name is {self.nickname} and he's {self.age} years old"


# class Cat(Animal):
#     def __init__(self, nickname, age, owner):
#         super().__init__(nickname, age)
#         self.owner = owner

#     def get_info(self):
#         return f"It's cat. His name is {self.nickname} and he's {self.age} years old"

#     def sound(self):
#         return f"{self.nickname} says Meow!"
    
# class Dog(Animal):
#     def __init__(self, nickname, age, owner):
#         super().__init__(nickname, age)
#         self.owner = owner

#     def get_info(self):
#         return f"It's a dog. His name is {self.nickname} and he's {self.age} years old"

#     def sound(self):
#         return f"{self.nickname} says Woof!"
    

# cat = Cat("Simon", 4, "Yurii")
# dog = Dog("Alisa", 7, "Vlad")

# # for animal in (cat, dog):
# #     if type(animal) is Dog:
# #         print(f"{animal.sound()} {animal.get_info()}")
# #     if isinstance(animal, Dog):
# #         print(f"{animal.sound()} {animal.get_info()}")

# # print(type(dog) is Dog)
# # print(isinstance(dog, Dog))

# print(isinstance(dog, Dog))
# print(isinstance(dog, Cat))
# print(isinstance(dog, Animal))

# print(type(dog) is Dog)
# print(type(dog) is Cat)
# print(type(dog) is Animal)

# print(super(Dog, dog).get_info())

"""
Method Resolution Order (MRO).
MRO в Python працює наступним чином:

1. Шукає атрибут серед атрибутів самого класу. Саме завдяки цьому, ми можемо "перевизначати" батьківські атрибуті.
2. Шукає атрибут в першого батька (той, що вказаний першим в списку батьків).
3. Шукає атрибут в наступного батька в списку батьків, поки такі є.
4. Шукає атрибут в батьках першого батька.
5. Повторює п.4 для всіх батьків.
6. Викликає виняток, якщо атрибут не знайдений.
"""

"""
A               E
    B       D
        C

"""

# class A:
#     pass

# class E:
#     pass

# class B(A):
#     pass

# class D(E):
#     pass

# class C(B, D):
#     pass

# print(C.mro())


"""
    A
C       B
    D
"""

# class A:
#     x = "a"

# class B(A):
#     x = "b"

# class C(A):
#     x = "c"

# class D(C, B):
#     def get_x(self):
#         return D.x
    
# print(D.mro())

# d = D()
# print(d.get_x())

# from collections import UserList
# from random import randint, choices


# class MyList(UserList):
#     info = "Це мій клас списку!!!"
#     my_list_var = [1, 2]

#     def get_positive(self):
#         return list(filter(lambda x: x >= 0, self.data))

#     def get_negative(self):
#         return list(filter(lambda x: x < 0, self.data))

#     def get_info(self):
#         return self.info

#     def get_my_list_var(self):
#         # return self.my_list_var
#         # return []
#         return MyList()
    
# r = []
# for _ in range(20):
#     r.append(randint(-5, 5))

# results = MyList(r)

# print(results)

# results2 = MyList(choices(range(-5, 6), k=20))
# print(results2)

# print(results.get_negative())
# print(results.get_positive())
# print(results.get_info())
# print(results.get_my_list_var())
# print(MyList.mro())

# from collections import UserDict

# contacts = [
#     {
#         "name": "Allen Raymond",
#         "email": "nulla.ante@vestibul.co.uk",
#         "phone": "(992) 914-3792",
#         "favorite": False,
#     },
#     {
#         "name": "Chaim Lewis",
#         "email": "dui.in@egetlacus.ca",
#         "phone": "(294) 840-6685",
#         "favorite": False,
#     },
#     {
#         "name": "Kennedy Lane",
#         "email": "mattis.Cras@nonenimMauris.net",
#         "phone": "(542) 451-7038",
#         "favorite": True,
#     },
#     {
#         "name": "Wylie Pope",
#         "email": "est@utquamvel.net",
#         "phone": "(692) 802-2949",
#         "favorite": False,
#     },
#     {
#         "name": "Cyrus Jackson",
#         "email": "nibh@semsempererat.com",
#         "phone": "(501) 472-5218",
#         "favorite": True,
#     }
# ]

# class Customer(UserDict):
#     def get_phone(self):
#         return f"{self.get('name')}: {self.get('phone')}"
    
# customers = [Customer(contact) for contact in contacts]

# for customer in customers:
#     print(customer.get_phone())

# from collections import UserString

# template = [
#     "Ви можете досягти всього. Варто лише трохи постаратися і запастися книгами.",
#     "Цей смартфон — справжня знахідка. Великий і яскравий екран, потужний процесор — все це в невеликому гаджеті.",
#     "Збирати камені нескінченності легко, якщо ви герой.",
#     "Освоїти верстку неважко. Візьміть книгу, нову книгу і повторіть всі приклади на практиці.",
#     "Боротися з прокрастинацією неважко. Просто дійте. Маленькими кроками.",
#     "Програмувати не настільки важко, як про це говорять.",
#     "Прості щоденні вправи допоможуть досягнути успіху."
# ]

# for i, comment in enumerate(template):
#     print("|{:^5}|{:<15}|".format(i, comment))


# class Comment(UserString):
#     def get_limit_contact(self, limit=10):
#         return f"{self.data[:limit-3]}..."
    
# comments = [Comment(comment) for comment in template]

# for i, comment in enumerate(comments):
#     print("|{:^5}|{:<15}|".format(i+1, comment.get_limit_contact(15)))

# card.py

from random import randint, sample
from collections import UserDict

class Card(UserDict):
    numbers_per_letter = 15 # розмір проміжку чисел для номерів в стовпці літери
    limit_line = 5  # кількість номерів в стовпці
    loto_fields = ["B", "I", "N", "G", "O"]

    def __init__(self):
        super().__init__() # Змушуємо відпрацювати конструктор UserDict, щоб це був словник
        self.start_num = 1 # починаємо працювати з 1
        self.end_num = self.start_num + self.numbers_per_letter # і виділяємо проміжок в 15 чисел
        # логіка для заповнення карточки
        self.create_card()
    
    def create_card(self):
        for letter in self.loto_fields: # Для кожної літери створюємо список рандомних номерів
            self.data[letter] = sample(range(self.start_num, self.end_num), k=self.limit_line)
            # Оновлюємо діапазон номерів для наступної літери
            self.start_num = self.end_num
            self.end_num = self.start_num + self.numbers_per_letter

    def pretty_info(self):
        print("{:^5}{:^5}{:^5}{:^5}{:^5}".format(*self.data))
        for i in range(self.limit_line):
            line = []
            for letter in self.loto_fields:
                line.append(self.data[letter][i])
            print("{:^5}{:^5}{:^5}{:^5}{:^5}".format(*line))
    
    def set_num_to_zero(self, num):
        for k, line in self.data.items():
            self.data[k] = list(map(lambda x: 0 if x == num else x, line))



# if __name__ == "__main__":
#     card = Card()
#     print(card)
#     card.pretty_info()


# gamer.py
class Gamer:
    def __init__(self, name, card):
        self.name = name
        self.card = card
        self.winner = False

    def check_winner(self):
        # перевірити вертикальні лінії карточки
        for col in self.card.values():
            if sum(col) == 0:
                self.winner = True
        
        # перевірити горизонтальні линії карточки
        for i in range(self.card.limit_line):
            row = []
            for key in self.card:
                row.append(self.card[key][i])
            if sum(row) == 0:
                self.winner = True

    def mark_number(self, num):
        self.card.set_num_to_zero(num)


# main.py

from random import randint
# from card import Card
# from gamer import Gamer

class LotoGame:
    def __init__(self, gamers):
        self.gamers = gamers # набір гравців для гри
        self.min_number = 1 # мінімальній номер першого шару (бочонку)
        self.max_number = Card.numbers_per_letter * Card.limit_line # максимальний номер останнього шару (бочонку) 75
        self.winners = [] # список переможців
        self.draw_numbers = [] # список випавших номерів
        self.progress = 0 # крок (прогрес) гри

    def start(self):
        while True:
            # крок гри
            self.step_game()
            # перевірити переможців
            self.check_winners()
            if self.winners:
                break
        return self.progress, self.winners
    

    def step_game(self):
        while True:
            current_num = randint(self.min_number, self.max_number)
            if current_num not in self.draw_numbers:
                self.draw_numbers.append(current_num)
                break
        self.progress += 1
        for gamer in self.gamers:
            gamer.mark_number(current_num)
            gamer.check_winner()

    def check_winners(self):
        for gamer in self.gamers:
            if gamer.winner:
                self.winners.append(gamer)


if __name__ == "__main__":
    players_names = ['Oleksandr', 'Volodymyr', 'Roman', 'Andrii', 'Borys', 'Iryna', 'Serhii', 'Nissa', 'Krabat', 'Oleh', 'Oleksandra']

    gamers = []
    for name in players_names:
        card = Card()
        gamer = Gamer(name, card)
        gamers.append(gamer)

    game = LotoGame(gamers)
    for gamer in gamers:
        print(gamer.name)
        gamer.card.pretty_info()
    quantity, winners = game.start()
    print(f"Кількість кроків {quantity}")
    print(f"Випавші номери {game.draw_numbers}")
    for winner in winners:
        print(f"Переможець {winner.name}")
        winner.card.pretty_info()