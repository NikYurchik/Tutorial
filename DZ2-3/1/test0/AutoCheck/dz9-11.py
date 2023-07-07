from functools import reduce

numbers = [3, 4, 6, 9, 34, 12]
sum = reduce(lambda x, y: x + y, numbers)
print(sum)

s = 0
for m in numbers:
    s += m
print(s)
