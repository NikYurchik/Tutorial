list_payment = [100, -3, 400, 35, -100]
res = []
for s in filter(lambda x: x >= 0, list_payment):
    res.append(s)
print(res)
