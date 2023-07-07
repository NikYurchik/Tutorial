import collections

Cat = collections.namedtuple("Cat", ["nickname", "age", "owner"])

cat_list = [Cat("Mick", 5, "Sara"), Cat("Barsik", 7, "Olga"), Cat("Simon", 3, "Yura")]

cat_dict = [
               {"nickname": "Mick", "age": 5, "owner": "Sara"},
               {"nickname": "Barsik", "age": 7, "owner": "Olga"},
               {"nickname": "Simon", "age": 3, "owner": "Yura"},
           ]

def convert_list(cats):
    res = []
    if isinstance(cats[0], type({})):
        for m in cats:
            res.append(Cat(m["nickname"], m["age"], m["owner"]))
    else:
        for m in cats:
            res.append({"nickname": m.nickname, "age": m.age, "owner": m.owner})
    return res

print(convert_list(cat_list))
print(convert_list(cat_dict))

