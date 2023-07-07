import re

string = "The resulting profit was: from the southern possessions $ 100, from the northern colonies $500, and the king gave $1000."

def generator_numbers(string=""):
    for v in re.findall('\d+', string):
        yield int(v)

print(re.findall('\d+', string))

sum = 0
for a in generator_numbers(string):
    sum += a

print(sum)

