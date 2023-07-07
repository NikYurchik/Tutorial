from functools import reduce

payment = [1, -3, 4]
sum = reduce(lambda x, y: x + y, filter(lambda x: x >= 0, payment))
print(sum)

s = 0
for m in payment:
    if m > 0:
        s += m
print(s)
