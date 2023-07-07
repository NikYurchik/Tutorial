def format_phone_number(func):
    def inner(phone):
        print(f'Source phone {phone}')
        result = func(phone)
        print(f'Sanitize: {result}')
        if len(result) == 10:
            phone_new = '+38' + result
        elif len(result) == 12:
            phone_new = '+' + result
        else:
            phone_new = result
        print(f'Result: {phone_new}')
        return phone_new
    return inner

@format_phone_number
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
"""
def sanitize_phone_number(phone):
    s = ''
    for v in phone:
        if v >= '0' and v <= '9':
            s = s + v
    return s  
"""
phones = ["    +38(050)123-32-34", "     0503451234", "(050)8889900", "38050-111-22-22", "38050 111 22 11   "]
for phone in phones:
    print('Result_phone ' + sanitize_phone_number(phone))
