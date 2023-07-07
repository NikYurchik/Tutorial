import os, sys, re, pathlib

txt = "Hello world!"
print(txt)

chars = ["a", "b", "c", "a"]
# chars = 'abca'
c_ind = chars.index("c")
print(c_ind)
c_ind = chars.index("e")
print(c_ind)

# real_dst = str(pathlib.Path.home().joinpath('Documents', 'Canada', '2024')) + '\\Cource_202304.pdf'
# print(real_dst)
# real_dst = os.path.dirname(real_dst)
# print(real_dst)
# if os.path.exists(real_dst):
#     print('Path exists')
# else:
#     print("Path doesn't exists")
# print(os.path.dirname(real_dst))

# print(sys.argv)
# for v in sys.argv:
#     print(v)

# arg = '123 qwerty "+1 (234) 567\'8900" 777' #pathlibinput('>> ')
# #cm = arg.split(' ')
# def split(arg, sep=' '):
#     cm = []
#     cv = ''
#     kv = ''
#     for i in range(len(arg)):
#         c = arg[i]
#         fl = (i == len(arg)-1 or arg[i+1] == sep)
#         if kv == '"':
#             if c == '"' and fl:
#                 cm.append(cv)
#                 cv = ''
#                 kv = ''
#             else:
#                 cv = cv + c
#         elif kv == "'" and fl:
#             if c == "'":
#                 cm.append(cv)
#                 cv = ''
#                 kv = ''
#             else:
#                 cv = cv + c
#         elif c in ('"', "'") and len(cv) == 0:
#             kv = c
#         elif c== sep and len(cv) > 0:
#             cm.append(cv)
#             cv = ''
#         else:
#             cv = cv + c
#     if len(cv) > 0:
#         cm.append(cv)
#     return cm

# for v in split(arg):
#     print(v)

# st = "Недопустимое значение '{value}' для настройки 'language'"
# print(st.replace('{value}', 'aa'))

# for key, val in sys.modules.items():
#     print(key+':',val)

# from pathlib import Path
# home_directory = Path.home().joinpath('Documents', 'bot', 'save')
# print( f'Path: { home_directory} !' )

"""
def accumulate():
    tally = 0
    while 1:
        next = yield
        if next is None:
            return tally
        tally += next

def gather_tallies(tallies):
    while 1:
        tally = yield from accumulate()
        tallies.append(tally)

tallies = []
acc = gather_tallies(tallies)
next(acc)  # Ensure the accumulator is ready to accept values
for i in range(4):
    acc.send(i)

acc.send(None)  # Finish the first tally
for i in range(5):
    acc.send(i)

acc.send(None)  # Finish the second tally

tpl = ('Hello', 'world')
print(type(txt))
print(type(tpl))
print(type(()))
# some_str = 'aaAbbB C F DDd EEe'
# for i in filter(lambda x: x.islower(), some_str):
#     print(i)
#print(destination_path)

for root, dirs, files in os.walk( '.\\test'):
    print(root)
    print(dirs)
    print(files)

s = "Привет!"

utf8 = s.encode()
print(utf8)  # b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82!'
s_from_utf8 = utf8.decode().casefold()

utf16 = s.encode('utf-16')
print(utf16)  # b'\xff\xfe\x1f\x04@\x048\x042\x045\x04B\x04!\x00'
s_from_utf16 = utf16.decode('utf-16').casefold()

print(s_from_utf8)
print(s_from_utf16)

import re
string = 'hello 12 hi 89. Howdy 34'
pattern = 'Hi|ho'

for result in re.finditer(pattern, string, re.IGNORECASE):
    print(result)

    
regex = r"[a-zA-Z]{1}[\w\.]+@[a-zA-z]+\.[a-zA-Z]{2,}"

test_str = "Ima.Fool@iana.org Ima.Fool@iana.o 1Fool@iana.org first_last@iana.org first.middle.last@iana.or a@test.com abc111@test.com.net"

matches = re.finditer(regex, test_str)

for match in matches:
    print(f"{match.group()} start: {match.start()} end: {match.end()}")

 'Ima.Fool@iana.org  Ima.Fool@iana.o 1Fool@iana.org    first_last@iana.org    first.middle.last@iana.or a@test.com abc111@test.com.net'
['Ima.Fool@iana.org',                'Fool@iana.org', 'first_last@iana.org', 'first.middle.last@iana.or',         'abc111@test.com']
[    'Fool@iana.org',                'Fool@iana.org', 'first_last@iana.org', 'first.middle.last@iana.or',         'abc111@test.com']

'Irma +380(67)777-7-771 second +380(67)777-77-77 aloha a@test.com abc111@test.com.net +380(67)111-777-777+380(67)777-77-787'
[    '+380(67)777-7-771',     '+380(67)777-77-77',                                                      '+380(67)777-77-78']
[    '+380(67)777-7-771',     '+380(67)777-77-77',                                                      '+380(67)777-77-787']

'The main search site in the world is https://www.google.com The main social network for people in the world is https://www.facebook.com But programmers have their own social network http://github.com There they share their code. some url to check https://www..facebook.com www.facebook.com '
['https://www.google.com', 'https://www.facebook.com', 'http://github.com']
['https://www.google.com', 'https://www.facebook.com', 'http://github.com', 'https://www..facebook.com']
  
"""
