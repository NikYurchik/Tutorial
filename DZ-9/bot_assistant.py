
"""
This is a bot-assistant.

Bot implemented as a console application.

After starting it displays 'I'm ready' and the invitation '>>'.

Executes commands:
'hello' - responds to 'How can I help you?'
'add <name> <phone>' - saves a new contact in the phonebook.
'change <name> <phone>' - saves the new phone number of an existing contact in the phonebook.
'phone <name>' - returns the phone number for the specified contact.
'show all' - displays all saved contacts with phone numbers.
'good bye', 'close', 'exit' - after any of these commands it outputs 'Good bye!' and completes its work.
"""

done = True

contacts = dict()

def input_error(func):
    def inner(argv):
        try:
            res = func(argv)
        except Exception as e:
           res = str ( e )
        return res
    return inner

def sanitize_phone_number(phone):
    result = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    if result.isdecimal():
        if len(result) == 10:
            phone_new = '+38' + result
        elif len(result) == 12:
            phone_new = '+' + result
        else:
            phone_new = result
    else:
        raise ValueError('The phone number must contain invalid characters!')
    return phone_new

def check_name_exists(name, flag=False):
    """
    Check if a contact's name is in the phone book.
    If flag = False and the name is not in the phone book, then there will be an error '.
    If flag = True and the name is in the phone book, then there will be an error '.
    """
    if contacts.get(name) == None:
        if not flag:
            raise ValueError('The contact name was not found in the phonebook!')
    else:
        if flag:
            raise ValueError('The contact name alredy exists in the phonebook!')

def fun_hello(argv):
    return 'How can I help you?'

@input_error
def fun__add(argv):
    ph = sanitize_phone_number(argv[1])
    nm = argv[0].capitalize()
    check_name_exists(nm, True)
    contacts.update({nm: ph})
    return 'Ok'

@input_error
def fun_change(argv):
    ph = sanitize_phone_number(argv[1])
    nm = argv[0].capitalize()
    check_name_exists(nm)
    contacts.update({nm: ph})
    return 'Ok'

@input_error
def fun_phone(argv):
    nm = argv[0].capitalize()
    check_name_exists(nm)
    return nm + ': ' + contacts.get(nm)

def fun_show_all(argv):
    st = 'Current phonebook:'
    for k, v in contacts.items():
        st = st + '\n' + k + ': ' + v
    return st

def fun_exit(argv):
    global done
    done = False
    return 'Good bye!'

"""
Dictionary of valid commands.
The key is the first word of the command.
Value - list of command details:
    [0] - allowable parameters in the command;
    [1] - additional command word;
    [2] - a function that executes a command.
"""
funcs = {
    "hello": [0, '', fun_hello],
    "add": [2, '', fun__add],
    "change": [2, '', fun_change],
    "phone": [1, '', fun_phone],
    "show": [1, 'all', fun_show_all],
    "good": [1, 'bye', fun_exit],
    "close": [0, '', fun_exit],
    "exit": [0, '', fun_exit]
}

def parcer(command):
    """
    Parser of the entered command.
    Input parameter - the entered command.
    If an empty string is entered or the command is not in the dictionary, then an error will be 'Unexpected command!'.
    If the command is in the dictionary, but the number of command parameters does not match the allowed one from 
    the command dictionary, then there will be an error 'Not enough parameters!' or 'Too many parameters!'.
    If all checks passed without errors, then the function corresponding to the command is called.
    Command parameters are passed as a list.
    The parser returns the strings returned by the functions to the main loop.
    """
    res = 'Unexpected command'
    if len(command) > 0:
        cm = command.split(' ')
        cm0 = cm[0].lower()
        lcm = len(cm) - 1
        lfn = funcs.get(cm0)
        if lfn == None:
            res = res + ' "' + cm[0] + '"!'
        else:
            ecm = lfn[0]
            if lcm < ecm:
                res = f'Not enough parameters! Expected {lcm}, received {ecm}.'
            elif lcm > ecm:
                res = f'Too many parameters! Expected {lcm}, received {ecm}.'
            elif len(lfn[1]) > 0 and cm[1].lower() != lfn[1]:
                res = res + ' "' + cm[0] + ' ' + cm[1] + '"!'
            else:
                if len(lfn[1]) > 0:
                    cm.pop(1)
                cm.pop(0)
                res = lfn[2](cm)
    else:
        res = res + '!'
    return res


def main():
    global done
    done = True
    print("I'm ready")
    while done:
        st = input('>> ')
        an = parcer(st)
        if len(an) > 0:
            print(an)

if __name__ == "__main__":
    main()
