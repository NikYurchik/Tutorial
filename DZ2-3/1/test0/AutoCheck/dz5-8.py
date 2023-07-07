grades = {"A": 5, "B": 5, "C": 4, "D": 3, "E": 3, "FX": 2, "F": 1}
students = {"Nick": "A", "Olga": "B", "Mike": "FX", "Anna": "C"}
"""
   1|Nick      |  A  |  5
   2|Olga      |  B  |  5
   3|Mike      | FX  |  2
   4|Anna      |  C  |  4
"""
def formatted_grades(students):
    i = 0
    s = ""
    res = list()
    for key, val in students.items():
        i += 1
        #print(i, key, val, grades.get(val))
        s = "{:>4}|{:<10}|{:^5}|{:^5}".format(i, key, val, grades.get(val))
        res.append(s)
    return res

for el in formatted_grades(students):
    print(el)
#print(formatted_grades(students))    
#print("|{:<10}|{:^10}|{:>10}|".format(1, 'center', 'right'))  # |left      |**center**|     right|
#formatted_grades(students)
# [' 1|Nick | A | 5 ', ' 2|Olga | B | 5 ', ' 3|Boris | FX | 2 ', ' 4|Anna | C | 4 ']
# [' 1|Nick | A | 5', ' 2|Olga | B | 5', ' 3|Boris | FX | 2', ' 4|Anna | C | 4']