from datetime import datetime, date

CYRILLIC_SYMBOLS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЄІЇҐабвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("A", "B", "V", "G", "D", "E", "E", "Zh", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U",
               "F", "H", "Ts", "Ch", "Sh", "Sch", "", "Y", "", "E", "Yu", "Ya", "Ye", "I", "Ji", "G",
               "a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "ye", "i", "ji", "g")
TRANSLATION_UKR = ("A", "B", "V", "H", "D", "E", "E", "Zh", "Z", "Y", "Y", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U",
                   "F", "Kh", "Ts", "Ch", "Sh", "Shch", "", "Y", "", "E", "Yu", "Ya", "Ye", "I", "Yi", "G",
                   "a", "b", "v", "h", "d", "e", "e", "zh", "z", "y", "i", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "iu", "ia", "ie", "i", "i", "g")
TRANS = {}
TRANSU = {}

def transliteration(text, is_ukr = False):
    global TRANS
    global TRANSU
    if is_ukr:
        if len(TRANSU) == 0:
            for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION_UKR):
                TRANSU[ord(c)] = l
        return(text.translate(TRANSU))
    else:
        if len(TRANS) == 0:
            for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
                TRANS[ord(c)] = l
        return(text.translate(TRANS))

def split(arg, sep=' '):
    cm = []
    cv = ''
    kv = ''
    for i in range(len(arg)):
        c = arg[i]
        fl = (i == len(arg)-1 or arg[i+1] == sep)
        if kv == '"':
            if c == '"' and fl:
                cm.append(cv)
                cv = ''
                kv = ''
            else:
                cv = cv + c
        elif kv == "'" and fl: 
            if c == "'":
                cm.append(cv)
                cv = ''
                kv = ''
            else:
                cv = cv + c
        elif c in ('"', "'") and len(cv) == 0:
            kv = c
        elif c== sep and len(cv) > 0:
            cm.append(cv)
            cv = ''
        else:
            cv = cv + c
    if len(cv) > 0:
        cm.append(cv)
    return cm

def get_date(sdate):
    fmd = ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%d%m%Y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y')
    dt = None
    if sdate == '':
        return ''
    for fm in fmd:
        try:
            dt = datetime.strptime(sdate, fm)
            break
        except ValueError:
            pass
    if dt is None:
        raise ValueError(f'The string "{sdate}" is not a date!')
    return dt.date()



"""international dialing codes"""
def format_phone_number(phone):
    def split(tail):
        c = tail if len(tail) <= 4 else tail[0:3] + '-' + tail[3:]
        return c
    
    s = phone
    if s[0] == '+':
        if s[1] == '1':
            phone_new = s[0:2] + '(' + s[2:5] + ')' + split(s[5:])
        elif s[1] == '2':
            if s[2] in ('0','7','8'):
                phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
            else:
                phone_new = s[0:2] + '-' + s[2:5] + '-' + split(s[5:])
        elif s[1] == '3':
            if s[2:5] == '735':
                phone_new = s[0:4] + '(' + s[4] + ')' + split(s[5:])
            elif s[2:6] in ('7321','7377'):
                phone_new = s[0:5] + '(' + s[5:7] + ')' + split(s[7:])
            elif s[2:4] == '80':
                phone_new = s[0:3] + '(' + s[3:6] + ')' + split(s[6:])
            elif s[2:7] == '90549':
                phone_new = s[0:3] + '(' + s[3:7] + ')' + split(s[7:])
            elif s[2:7] == '906698':
                phone_new = s[0:3] + '(' + s[3:5] + '-' + s[5:8] + ')' + split(s[8:])
            elif s[2] in ('5','7','8'):
                phone_new = s[0:4] + '-' + s[4:7] + '-' + split(s[7:])
            else:
                phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
        elif s[1] == '4':
            if s[2] == '2':
                phone_new = s[0:4] + '-' + s[4:7] + '-' + split(s[7:])
            elif s[2:7] in ('41481','41534','41624'):
                phone_new = s[0:3] + '(' + s[3:7] + ')' + split(s[7:])
            else:
                phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
        elif s[1] == '5':
            if s[2:5] in ('993','994','997','999'):
                phone_new = s[0:5] + '-' + s[5:7] + '-' + split(s[7:])
            elif s[2] in ('0','9'):
                phone_new = s[0:4] + '-' + s[4:7] + '-' + split(s[7:])
            else:
                phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
        elif s[1] == '6':
            if s[2:6] == '1891':
                phone_new = s[0:3] + '(' + s[3:6] + ')' + split(s[6:])
            elif s[2] in ('7','8','9'):
                phone_new = s[0:4] + '-' + s[4:7] + '-' + split(s[7:])
            else:
                phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
        elif s[1] == '7':
            phone_new = s[0:2] + '(' + s[2:5] + ')' + split(s[5:])
        elif s[1] == '8':
            if s[2:5] in ('816','817','818','819'):
                phone_new = s[0:5] + '-' + s[5:7] + '-' + split(s[7:])
            elif s[2:6] == '8216':
                phone_new = s[0:6] + '-' + split(s[6:])
            elif s[2] in ('0','3','5','7','8','9'):
                phone_new = s[0:4] + '-' + s[4:7] + '-' + split(s[7:])
            else:
                phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
        elif s[1] == '9':
            if s[2:6] == '0392':
                phone_new = s[0:3] + '(' + s[3:6] + ')' + split(s[6:])
            elif s[2] in ('6','7','9'):
                phone_new = s[0:4] + '-' + s[4:7] + '-' + split(s[7:])
            else:
                phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
    else:
        phone_new = s[0:3] + '-' + s[3:6] + '-' + split(s[6:])
    return phone_new

def sanitize_phone_number(phone):
    ph = phone.strip()
    pl = '+' if ph[0] == '+' else ''
    s = ''
    for v in ph:
        if v >= '0' and v <= '9':
            s = s + v
    if ph[0] != '+':
        if len(s) == 10 and s[0] == '0':
            s = '+38' + s
        elif len(s) > 10:
            s = '+' + s
    else:
        s = pl + s
    return s  
