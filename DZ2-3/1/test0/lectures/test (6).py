# import random

# a = list(range(20))
# random.shuffle(a)
# a.append(random.choice(a))

# print(a)
# def my_sort(l):
#     print(f"l is now: {l}")
#     if not l:
#         return l
#     middle = l[len(l) // 2]
#     middle_l = [x for x in l if x == middle]
#     less_middle = [x for x in l if x < middle]
#     bigger_middle = [x for x in l if x > middle]
#     return my_sort(less_middle) + middle_l + my_sort(bigger_middle)

# print(5)

# print(my_sort(a))


# d = {
#     "root":{
#         1: {
#             3: {
#                 5: 50,
#                 6: 60
#             },
#             9: [45, 46]
#         },
#         2: {
#             4: {
#                 7: 70,
#                 8: 80
#             }
#         }
#     }
# }

# print(d)

# def walk_tree(d):
#     if isinstance(d, dict):
#         res = []
#         for k, v in d.items():  
#             res.append(k)
#             res.extend(walk_tree(v))
#         return res
#     elif isinstance(d, list) or isinstance(d, tuple):
#         return d
#     else:
#         return [d]
    

# print(walk_tree(d))

# examples = (
#     "3 4 +",
#     "2 4 * 8 + ",
#     "2 4 8 + * ",
#     "3 2 * 11 -",
#     "2 5 * 4 + 3 2 * 1 + / "
# )
# operators = ("+", "-", "*", "/")

# def solve_rpn(example):
#     stack = []
#     for x in example:
#         if x in operators:
#             second = stack.pop()
#             first = stack.pop()
#             r = f"{first}{x}{second}"
#             stack.append(eval(r))
#         else:
#             stack.append(x)
#     return stack[0]

# def solve_rpn(example):
#     if len(example) == 3:
#         return eval(f"{example[0]}{example[2]}{example[1]}")
#     i = 2
#     while i < len(example) and example[i] not in operators:
#         i += 1
#     return solve_rpn(example[:i-2] + [str(solve_rpn(example[i-2:i+1]))] + example[i+1:])



# for example in examples:
#     print(solve_rpn(example.split()))

# Чому в цьому рішення завдання(Модуль 6 Завдання 5/14). a1 перебирає строки як str(), a перебирає строки та бере останій результат?
# def get_cats_info(path):
#     split_line = []
#     a = []
#     a1 = []
#     with open(path, "r") as fh:
#         while True:
#             line = fh.readline()
#             if not line:
#                 break

#             split_line = line.split(",")
#             res_line = {}

#             res_line["id"] = split_line[0]
#             res_line["name"] = split_line[1]
#             res_line["age"] = split_line[2].replace("\n", "")

#             print(id(res_line))

#             a1.append(str(res_line))
#             a.append(res_line)
#     print(a1)
#     print(a)

# get_cats_info("m08_03_1-5_recap/file.txt")

# виходить що в рекурсию функцii можна не тiльки значення передавати (наприклад "flatten(i)" ), а ще вставляти функцiю в такi методи як res.extend(flatten(i))? або наприклад append (flatten(i))?  
# def flatten(data):
#     res = []
#     for i in data:
#         if type(i) is list:
#             result = flatten(i)
#             res.extend(result)
#         else:
#             res.append(i)
#     return res
# x = flatten([1, [2, 3], [4, [5, [6, 7]]], [[[8], 9], [10]]])
# print(x)

# res = []
# def flatten(data):
#     res = []
#     for i in data:
#         if type(i) is list:
#             res.extend(flatten(i))
#         else:
#             res.extend([i])
#     return res
# Чому коли ми вставляемо змiнну всередину функii, то у нас "res" зберiгае тiльки останнiй результат? а не так як с глобальною res 
# x = flatten([1, [2, 3], [4, [5, [6, 7]]], [[[8], 9], [10]]])
# print(x)

from pathlib import Path
from collections import Counter
from datetime import datetime as dt

p = Path(__file__)
# print(p)
# print(p.parent)
# print(list(p.parents))
# print(p.name)
# print(p.suffix)
# print(p.stem)
# print(p.anchor)
# print(p.is_absolute())
# print(p.absolute())
# print(p.is_relative_to("/home"))
# print(p.relative_to("/home/illia/"))
# print(p.joinpath("test", "test.py"))
# print(p.match("*/*_*/*.py")) # m08_03_1-5_recap
# print(p.with_name("test2.txt"))
# print(p.with_stem("fsdf"))
# print(p.with_suffix(".js"))
# print(p.with_suffix(""))
# print(list(p.parent.iterdir()))
# print(p.with_suffix(".js").exists())
# p.with_suffix("").joinpath("test2").mkdir(parents=True, exist_ok=False)
# p.with_stem("test2").touch(exist_ok=True)
# p.with_name("test30.txt").touch()
# p.with_stem("test2").rename(p.with_name("test30.txt"))
# print(p.read_text())
# p.with_name("test30.txt").write_text("testtest")
# p.with_name("test30.txt").unlink()
# print(Counter(path.suffix for path in p.parent.iterdir()))
# print(Counter(path.suffix for path in p.parent.glob("*.p*")))

# Displaying a Directory Tree
# display_dir_tree.py

# def tree(directory):
#     res = []
#     res.append(f"+ {directory}")
#     for path in sorted(directory.glob("**/*")):
#         depth = len(path.relative_to(directory).parts)
#         spacer = "    " * depth
#         res.append(f"{spacer}+ {path.name}")
#     return res

# Path(__file__).with_name("result.txt").write_text("\n".join(tree(Path.cwd())))
# tree(Path.cwd())

# Creating a Unique Filename
# unique_path.py

# def unique_path(directory, name_pattern):
#     counter = 0
#     while True:
#         counter += 1
#         path = directory / name_pattern.format(counter)
#         if not path.exists():
#             path.touch()
#             return path

# print(unique_path(p.parent, "test{:03d}.txt"))


# import sys

# print(sum((float(x) for x in sys.argv[1:])))
# print(sys.version)
# # sys.exit("test")
# print(sys.path)
# a = 4
# b = "test"
# c = 8.5
# d = True
# print(sys.getrefcount(a))
# print(sys.getrefcount(b))
# print(sys.getrefcount(c))
# print(sys.getrefcount(d))
# # sys.setrecursionlimit(5)
# print(sys.getrecursionlimit())
# print(sys.getdefaultencoding())

# def sum_num(num):
#     sum = 0
#     for n in num:
#         sum += int(n)
#     if len(str(sum)) == 1:
#         return sum
#     return sum_num(str(sum))


# num = input("Enter a number: ")
# print(sum_num(num))


# for i in range(5):
#     for j in range(10):
#         print(i, j)

# n = 0
# while n < 10:
#     print(n)
#     n += 1

# a = list(range(5))
# print(a)
# d = {k: v for k in range(3) for v in "abc"}
# print(d)
# try:
#     # b = a[5]
#     # c = d[4]
#     with open("tttt.txt") as f:
#         print(f.read())
# except (IndexError, KeyError, FileNotFoundError) as e:
#     print(e)
    # b = a[-1]

# print(b)

# def test(*args, **kwargs):
#     print(args)
#     print(kwargs)


# a = tuple(x for x in range(10))
# # print(a)
# test(1, a=5)
# test(1, 2, b=6, e=9)
# test(1, 2, 3, c=7, f="test")
# test(*a, d=8, is_true=True)
# # b = tuple(x for x in range(3))
# # r, t, b = b
# # print(r, t, b)
# d = {"a": 1, "test": False, "56": 65}
# print(d)
# test(**d)
# test(*a, **d)

# l = [f"{a}{b}{c}" for a in "test" for b in "hello" for c in "world"]
# print(l)
# s = "|||||".join(l)

# print(s.split("|||||"))


# if __name__ == "__main__":
#     print(__file__)
#     print(__name__)
#     import a

# def append_to_list(a, l=None):
#     if not l:
#         l = []
#     l.append(a)
#     print(l)

# my_list = [x for x in range(10)]
# print(my_list)
# append_to_list(5, my_list)
# # print(my_list)
# append_to_list(6)
# # print(my_list)
# append_to_list("test")
# print(my_list)


# from datetime import datetime as dt

# now = dt.now()
# d = {
#     now: "test"
# }
# print(d)