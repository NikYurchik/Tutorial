import re
"""
    'result': True,
    'first_index': 34,
    'last_index': 40,
    'search_string': 'Python',
    'string': 'Guido van Rossum began working on Python in the late 1980s, as a successor to the 
"""

def find_word(text, word):
    res = {}
    match = re.search(word, text)
    if match:
        res.update({'result': True})
        res.update({'first_index': match.start()})
        res.update({'last_index': match.end()})
    else:
        res.update({'result': False})
        res.update({'first_index': None})
        res.update({'last_index': None})

    res.update({'search_string': word})
    res.update({'string': text})
    return res

print(find_word(
    "Guido van Rossum began working on Python in the late 1980s, as a successor to the ABC programming language, and first released it in 1991 as Python 0.9.0.",
    "Python"))
