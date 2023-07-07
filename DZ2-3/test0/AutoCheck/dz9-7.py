name = ["dan", "jane", "steve", "mike"]
#for s in map(lambda x: x[0].upper() + x[1:], name):
for s in map(lambda x: x.capitalize(), name):
    print(s)
