"""
Метод: find
----
Даний рядок символів.
Видалити з цього рядка групи символів, розташованих між квадратними дужками [, ].
Самі дужки теж мають бути видалені.
Припустимо, що всередині кожної пари дужок немає інших дужок.
"""

# string = "Видалити з цього [рядка групи] символів, [розташованих між] квадратними дужками [, ]."

# def sanitize(string):
#     new_string = string[:]
#     while True:
#         print(new_string)
#         start_index = new_string.find("[")
#         end_index = new_string.find("]")
#         if start_index == -1 or end_index == -1:
#             break
#         new_string = new_string[:start_index] + new_string[end_index+1:]
#     return new_string

# print(sanitize(string))

"""
Метод: isdigit
----
1. Знайти кількість цифр в рядку
2. Знайти кількість чисел в рядку
"""

# string = "1 цифра 23 число текст текст текст. Я мав 1 яблуко, отримав ще 99, отримав 100. 567"

# def count_digits(string):
#     count = 0
#     for el in string:
#         if el.isdigit():
#             count += 1
#     return count

# # print(count_digits(string))

# def count_numbers(string):
#     count = 0
#     nums = []
#     pos = 0
#     while pos < len(string):
#         if string[pos].isdigit():
#             num = ''
#             while pos < len(string) and string[pos].isdigit():
#                 num += string[pos]
#                 pos += 1
#             nums.append(num)
#             count += 1
#         else:
#             pos += 1
#     return count, nums

# print(count_numbers(string))
"""
url = url.split(';') 
dict1 = {} 
for i in url: 
    index_ = i.index('=') 
    dict1.update({
        i[:index_] : i[index_ + 1 :]
        }) 
print(dict1)

url_query = "20850=ot-25-mp-do-47-mp;23777=6-6-5;38435=8-gb;41404=16gb" 
query_params = url_query.split(';') 
print(query_params) 
"""


"""
Метод: split, join
----
Розбираємо URL с Rozetka
"""

# url_query = "20850=ot-25-mp-do-47-mp;23777=6-6-5;38435=8-gb;41404=16gb"

# query = url_query.split(";")

# obj_query = {}
# for el in query:
#     key, value = el.split("=")
#     obj_query.update({
#         key: value
#     })

# print(obj_query)

# prepare = []
# for key, value in obj_query.items():
#     prepare.append(key + "=" + value) # f"{key}={value}"

# print(";".join(prepare))


"""
Методи: split, replace
----
Парсимо query запит для Google. Тут класичний сепаратор & і перетворюємо в словник з даними
"""

# url_search = "https://www.google.com/search?q=Cat+and+dog&ie=utf-8&oe=utf-8&aq=t"

# _, query = url_search.split("?")

# print(query)

# obj_query = {}

# for el in query.split("&"):
#     key, value = el.split("=")
#     obj_query.update({
#         key: value.replace("+", " ")
#     })

# print(obj_query)

"""
Метод Translate
"""

# map = {ord('й'): 'y', ord('Ю'): 'yu', ord('я'): 'ya', ord('ш'): 'sh'}

# translated = 'Юля йшла а я біг, незабаром буде шторм'.translate(map)

# print(translated)

import re

string = "Нільс Бор народився в родині професора фізіології Копенгагенського університету Християна Бора (1858—1911) й Еллен Адлер (1860—1930). Батьки Бора одружилися 1881 року. Батька Нільса Бора двічі висували кандидатом на Нобелівську премію з фізіології або медицини[11]. Мати була донькою впливового та вельми заможного єврейського банкіра і парламентаря-ліберала Давида Баруха Адлера[da] (1826—1878) і Дженні Рафаел (1830—1902) із британської єврейської банкірської династії Raphael Raphael & sons[en][12]. [5]"

# pattern = "[0-9]+"
# result = re.search(pattern, string)
# print(result.span())
# fi, li = result.span()
# print(result.group())

# result = re.findall(r'\d', string)
# print(result)
# print(len(result))

# result = re.findall(r'\d+', string)
# print(result)
# print(len(result))

# result = re.findall(r'\d{4}', string)
# print(result)
# print(len(result))

# pattern = r'[А-ЯA-Z]\w*'
# pattern = re.compile(r'[А-ЯA-Z]\w*')

# result = re.findall(pattern, string)
# result = pattern.findall(string)
# print(result)
# print(len(result))

# pattern = re.compile(r'\w+')

# result = pattern.findall(string)

# print(result)
# print(len(result))

# pattern = re.compile(r'[А-ЯA-Z]\w*$')

# result = pattern.findall(string)

# print(result)
# print(len(result))

# num = '18'
# pattern = rf'{num}\d\d'
# print(re.findall(pattern, string))

# print(re.sub(r'\[\d+\]', '', string))

print(re.findall(r'\b[А-Яа-яA-Za-z]{2}', string))


# Не понимаю почему не проходит код 
grades = {"A": 5, "B": 5, "C": 4, "D": 3, "E": 3, "FX": 2, "F": 1}

def formatted_grades(students):
    grades = {"A": 5, "B": 5, "C": 4, "D": 3, "E": 2, "FX": 2}

    rows = ["{:^4}|{:<10}|{:^5}|{:^5}".format(i + 1, name, grade, grades.get(grade, 0)) for i, (name, grade) in enumerate(students.items())]

    return rows


students = {"Nick": "A", "Olga": "B", "Mike": "FX", "Anna": "C"}

for el in formatted_grades(students):
    print(el)

# результат такой:
# Code output:
#  1  |Nick      |  A  |  5  
#  2  |Olga      |  B  |  5  
#  3  |Mike      | FX  |  2  
#  4  |Anna      |  C  |  4  
# Так же само и в задании
# Получалась следующая таблица:

#    1|Nick      |  A  |  5
#    2|Olga      |  B  |  5
#    3|Mike      | FX  |  2
#    4|Anna      |  C  |  4