def formatted_numbers():
    res = list()
    s = "|{:^10}|{:^10}|{:^10}|".format('decimal','hex','binary')
    res.append(s)
    for i in range(16):
        s = "|{:<10}|{:^10x}|{:>10b}|".format(i, i, i)
        res.append(s)
    return res

for el in formatted_numbers():
    print(el)
