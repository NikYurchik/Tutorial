import re
"""
    'result': True,
    'first_index': 34,
    'last_index': 40,
    'search_string': 'Python',
    'string': 'Guido van Rossum began working on Python in the late 1980s, as a successor to the 
"""
def replace_spam_words(text, spam_words):
    s = '('
    r = ''
    p = text
    for w in spam_words:
        s = s + r + w
        r = '|'
    s = s + ')'
    for res in re.finditer(s, text, re.IGNORECASE):
        t1 = "{:*^" + str(len(res.group())) + "}"
        t1 = t1.format('*')
        p = re.sub(res.group(), t1, p, flags = re.IGNORECASE)
    return p

print(replace_spam_words('blue socks and red shoes',('blue','red')))