def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


def get_phone_numbers_for_countries(list_phones):
    res = {}
    jp = list()
    sg = list()
    tw = list()
    ua = list()
    for v in list_phones:
        n = sanitize_phone_number(v)
        if n.startswith('81'):
            jp.append(n)
        elif n.startswith('65'):
            sg.append(n)
        elif n.startswith('886'):
            tw.append(n)
        else:
            ua.append(n)
    res.update({'UA': ua})
    res.update({'JP': jp})
    res.update({'TW': tw})
    res.update({'SG': sg})
    return res            
        
print(get_phone_numbers_for_countries(('+38(067)576-14-90','(095)0016-123','+81(23)456789','+65(123)456789','886(1)23456')))
        
            
    