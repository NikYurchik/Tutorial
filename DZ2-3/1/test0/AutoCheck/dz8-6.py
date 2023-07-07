from decimal import Decimal, getcontext


def decimal_average(number_list, signs_count):
    getcontext().prec = signs_count
    res = Decimal(0.0)
    for n in number_list:
        res = res + Decimal(n)
    res = res / Decimal(len(number_list))
    return res

print(decimal_average([3, 5, 77, 23, 0.57], 6)) # 21.714
print(decimal_average([31, 55, 177, 2300, 1.57], 9)) # 512.91400
#print(get_random_winners(quantity, participants))