pn = ['1101', '9034', '0011', '11a1']

def is_valid_pin_codes(pin_codes):
    if len(pin_codes) == 0:
        return 'Empty'
    for i in pin_codes:
        s = str(type(i))
        if s.find("'str'") < 0:
            return 'No Str' 
        if len(i) != 4:
            return 'Bad Lenght'
        if pin_codes.count(i) > 1:
            return 'No Unique'
        
        # try:
        #     k = int(i)
        # except:
        #     return 'No Number'
        if not i.isdecimal():
            return 'No Number'
    
    return 'True'

print(is_valid_pin_codes(pn))