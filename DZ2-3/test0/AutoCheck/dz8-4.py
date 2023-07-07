from random import randrange, sample


def get_numbers_ticket(min, max, quantity):
    res = []
    if min >= 1 and max <= 1000 and quantity > min and quantity < max:
        res = sample(range(min, max+1), k=quantity)
    res.sort()
    return res

print(get_numbers_ticket(1, 49, 6))
