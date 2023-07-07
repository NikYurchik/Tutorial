# Функція як об'єкт першого класу

# Перша умова - функція може бути збережена в змінній або структурі даних

# def mul(a, b):
#     return a * b

# f = mul
# result = f(2, 3)
# print(result)

# field = {
#     "a": 2,
#     "b": 3,
#     "ops": f
# }

# result = field.get("ops")(field.get("a"), field.get("b"))
# print(result)

# result = field.get("ops")(2, 3)
# print(result)

# Функція як об'єкт першого класу

# Друга умова - функція може бути передана в іншу функцію як аргумент

# def mul(a, b):
#     return a * b

# def sum(a, b):
#     return a + b

# def ops(a, b, func):
#     return func(a, b)

# result = ops(2, 3, mul)
# print(result)

# result = ops(2, 3, sum)
# print(result)

# Третя умова - функція може бути повернена з функції як результат

# def mul(a, b):
#     return a * b

# def sum(a, b):
#     return a + b

# def ops(operator):
#     if operator == "*":
#         return mul
#     elif operator == "+":
#         return sum
#     else:
#         raise ValueError("operator is not supported")
    

# try:
#     f_mul = ops("*")
#     result = f_mul(2, 4)
#     print(result)
# except ValueError:
#     print("cannot multiply")

# try:
#     f_add = ops("+")
#     result = f_add(2, 4)
#     print(result)
# except ValueError:
#     print("cannot add")


# try:
#     f_div = ops("/")
#     result = f_div(2, 4)
#     print(result)
# except ValueError:
#     print("cannot divide")

# Closures

# Особливість існування вкладених локальних просторів імен і той факт, що вони створюються динамічно,
# дає можливість використовувати механізм замикань в Python.

# def greeting(name):
#     def message(msg):
#         return f"{name} - {msg}"
#     return message

# msg_for_illia = greeting("Illia")
# msg_for_anna = greeting("Anna")

# print(msg_for_illia("Hello"))
# print(msg_for_anna("Goodbye!"))

# def taxer(base_tax):
#     def calculate(money):
#         nonlocal base_tax
#         if money >= 10_000:
#             base_tax = base_tax * 1.5  # base_tax *= 1.5
#             print(base_tax)
#         return money - base_tax * money
#     return calculate


# ukr = taxer(0.1)
# swd = taxer(0.55)

# m_u = ukr(5000)
# m_s = swd(25000)

# print(m_u, m_s)

# Кешування із замиканням
# def factorial_with_cache():
#     cache = {}
#     def calc(n):
#         if n < 0:
#             raise ValueError("Number must not be negative")
        
#         result = 1
#         for val in range(1, n + 1):
#             if val in cache:
#                 result = cache[val]
#             else:
#                 result = val * cache.get(val - 1, 1)
#                 cache[val] = result
#                 print(f"{val} was not in cache - {result}")

#         return result
#     return calc

# factorial = factorial_with_cache()
# f3 = factorial(3)
# print("----------------")
# f5 = factorial(5)
# # print()

# another_factorial = factorial_with_cache()
# another_factorial(4)

# print(id(factorial), id(another_factorial))

# def factorial(n, cache=None):
#     if not cache:
#         cache = {}
    
#     if n < 0:
#         raise ValueError("Number must not be negative!")
    
#     def calc(n):
#         result = 1
#         for val in range(1, n + 1):
#             if val in cache:
#                 result = cache[val]
#             else:
#                 result = val * cache.get(val - 1, 1)
#                 cache[val] = result
#                 print(f"{val} was not in cache - {result}")
#         return result
#     return calc(n)

# f3 = factorial(3)
# f5 = factorial(5)
# factorial(4)

# Каррування — це перетворення функції з багатьох аргументів в набір функцій, кожна з яких є
# функцією з одного аргументу. Ми можемо передати частину аргументів у функцію і отримати у відповідь функцію,
#  що очікує решту аргументів.

# def greeting_simple(name, msg):
#     return f"{name} - {msg}"

# print(greeting_simple("Bob", "Go to work!"))
# print(greeting_simple("Bob", "Goodnight!"))


# def greeting(name):
#     def message(msg):
#         return f"{name} - {msg}"
#     return message

# msg_for_bob = greeting("Bob")
# print(msg_for_bob("Go to work!"))
# print(msg_for_bob("Goodnight!"))

# def taxer_simple(base_tax, money):
#     if money >= 10000:
#         base_tax *= 1.5
#     return money - base_tax * money

# m_u = taxer_simple(0.1, 5000)
# m_s = taxer_simple(0.1, 25000)
# print(m_u, m_s)


# def taxer(base_tax):
#     def calculate(money):
#         nonlocal base_tax
#         if money >= 10000:
#             base_tax *= 1.5
#         return money - base_tax * money
#     return calculate

# ukr = taxer(0.1)
# m_u = ukr(5000)
# m_u2 = ukr(10_000)
# m_s = ukr(25000)
# print(m_u, m_s, m_u2)

# Декоратори
# Шаблон проєктування, створений для того, щоб розширити існуючий функціонал
# без змін в код цього самого функціоналу.



# def greeting_decorator(func):
#     def wrapper(*args, **kwargs):
#         print("Hello!")
#         result = func(*args, **kwargs)
#         print("Good bye!")
#         return result
#     return wrapper

# @greeting_decorator
# def greeting(val):
#     print(f"My name is {val}")


# greeting("Bob")

# Приклад Декоратору без *args, **kwargs

# def decorator_name(func):
#     def wrapper(name, surname):
#         result = func(name, surname)  # func = full_name
#         print("bye")
#         return result
#     return wrapper

# def prefix_decorator_name(func):
#     def wrapper(name, surname):
#         print("Prefix!")
#         name = f"Mr. {name}"
#         result = func(name, surname)  # func == decorator_name -> wrapper
#         print("Prefix ends....")
#         return result
#     return wrapper


# @prefix_decorator_name
# @decorator_name
# def full_name(name, surname):
#     print(f"Hello {name} {surname}")


# full_name("John", "Doe")


# Створити декоратор, що повертає кортеж з результатом функції і часом її виконання

# from time import time, sleep

# def time_counter(func):
#     def interval(*args, **kwargs):
#         start = time()
#         result = func(*args, **kwargs)
#         end = time()
#         passed = end - start
#         return result, passed
#     return interval

# @time_counter
# def test_func(a, b):
#     sleep(b)
#     return a + b

# # print(test_func(3, 5))


# @time_counter
# def factorial(n, cache={}):
#     if n < 0:
#         raise ValueError('Number not be negative')

#     def calc(n):
#         result = 1
#         for val in range(1, n + 1):
#             if val in cache:
#                 result = cache[val]
#             else:
#                 result = val * cache.get(val - 1, 1)
#                 cache[val] = result
#         return result

#     return calc(n)


# f3 = factorial(1300)
# print(f'f3: {f3}')

# f5 = factorial(1300)
# print(f'f5: {f5}')

# print(factorial(4))


#  Декоратор з назвою

# def decorator_with_name(name):
#     def wrapper(func):
#         def inner(*args, **kwargs):
#             print(f"Decorator: {name}")
#             result = func(*args, **kwargs)
#             return result
#         return inner
#     return wrapper

# @decorator_with_name("Big decorator")
# def adder(x, y):
#     return x + y


# @decorator_with_name("Small decorator")
# def mul(x, y=10):
#     return x * y


# print(adder(3,4))
# print(mul(3, y=3))
# print(mul(3))

# Лямбда функція

# def sq_normal(x):
#     return x ** 2

# sq = lambda x: x ** 2
# print(sq_normal(5))
# print(sq(5))

# print((lambda: "TODO")())

# Map

# names = ["dan", "jane", "steve", "mike"]

# def normalize(name):
#     return name.title()

# new_names = []
# for name in names:
#     # new_names.append(normalize(name))
#     new_names.append(name.title())
# print(new_names)

# new_names = map(normalize, names)
# print(list(new_names))

# new_names = map(str.title, names)
# print(list(new_names))

# new_names = map(lambda name: name.title(), names)
# print(list(new_names))

# new_names = [name.title() for name in names]
# print(list(new_names))

# payment = [100, -3, 400, 35, -100]

# def is_negative_number(num):
#     if num < 0:
#         return True
#     return False

# p_values = filter(is_negative_number, payment)
# print(list(p_values))

# p_values = filter(lambda num: num > 0, payment)
# print(list(p_values))

# nums = [i for i in range(1, 10)]
# print(nums)
# sq = map(lambda x: x ** 2, nums)
# # print(list(sq))
# result = filter(lambda value: value % 2, sq)
# print(list(result))

# result = map(lambda x: x ** 2, filter(lambda value: value % 2, [i for i in range(1, 10)]))
# print(list(result))


"""
Додаткові приклади!
"""
# Простий генератор

# def simple_gen():
#     yield 'First'
#     yield 'Second'


# for r in simple_gen():
#     print(r)

# -------------------------------------------------------------
# Самостійний виклик за допомогою next

# def simple_gen():
#     yield 'First'
#     yield 'Second'


# gen = simple_gen()
# print(gen)

# r = next(gen)
# print(r)

# r = next(gen)
# print(r)

# r = next(gen)
# print(r)

# -------------------------------------------------------------
# Свій генератор range

# def my_range(limit):
#     value = 0
#     while value < limit:
#         yield value
#         value = value + 1


# for num in range(5):
#     print(num)

# for num in my_range(5):
#     print(num)

# gen = my_range(5)

# while True:
#     try:
#         r = next(gen)
#         print(r)
#     except StopIteration:
#         break

# print('The end')


# -------------------------------------------
# Generator as Comprehension

# sq_gen = (i ** 2 for i in range(10))
# print(sq_gen)

# for i in sq_gen:
#     print(i, ' ', end='')

# ------------------------------------------------------
"""
Генератор, що вертає ціле число між min_val і max_val в нескінченному циклі
"""

# from random import randint


# def cycle_random_gen(min_val, max_val):
#     # BEGIN SOLUTION
#     while True:
#         yield randint(min_val, max_val)
#     # END SOLUTION


# rand_gen = cycle_random_gen(5, 15)

# result = []
# for _ in range(20):
#     value = next(rand_gen)
#     result.append(value)

# print(result)


# result_2 = []
# for _ in range(10):
#     value = next(rand_gen)
#     result_2.append(value)

# print(result_2)

# -----------------------------------------------------------
"""
Напишіть генератор, що повертає всі непарні квадрати від 0 до певного ліміту, використовуючи filter, lambda и map
"""

# MAX_VALUE = 10

# result = map(lambda x: x ** 2, filter(lambda value: bool(value % 2), list(range(MAX_VALUE))))


# def result_generator(limit):
#     for i in range(limit):
#         value = i ** 2
#         if value % 2:
#             yield value


# result_y = result_generator(MAX_VALUE)

# list_result = list(result)
# print(list_result)
# print(list_result)

# print(list(result_y))
# print(list(result_y))
