import os
import pathlib
import json
import re
from collections import UserList, UserDict
from datetime import datetime, date
from botsetting import CommandCancel, Bot_setting, get_number_of_days, get_display_lines, get_language
from bot_utils import format_phone_number, sanitize_phone_number, get_date
"""

"""
sep = '---------------------------------------------------------------'

messages = {
    'en': {
        'name_req': 'Name required!',
        'name_30': 'The name must be no more than 30 characters!',
        'bad_phone': 'Incorrect phone number "{value}"!',
        'bad_email': 'Incorrect email "{value}"!',
        'bad_fullname': 'Incorrect Full Name!',
        'phone_ex': 'Phone "{value}" alredy exists!',
        'phone_no': 'Phone "{value}" not found!',
        'email_ex': 'Email "{value}" alredy exists!',
        'email_no': 'Email "{value}" not found!',
        'com_cancel': "Command canceled.",
        'bad_key_com': 'Invalid key --{key} for command {command}',
        'bad_command': 'Command "{command}" is not defined for AddressBook.',
        'record_ex': 'Record "{vname}" alredy exists!',
        'record_no': 'Record "{vname}" not found!',
        'con_list': 'Contacts list',
        'bd_list': "List of contacts who have a birthday in the next {days} days",
        'bd_no': "There are no contacts whose birthdays are in the next {days} days.",
        'bd_days': "(before birthday {dtb} days)",
        'un_command': 'Unknown command "{command}".',
        'maybe_com': " Maybe you meant: {maybe}.",
        'hello': 'Hello! \nHow can I help you?',
        'good_bye': 'Good bye!',
        'dest_folder': "Enter the path where to sort (by default to the same folder):"
    },
    'ru': {
        'name_req': 'Имя обязательно!',
        'name_30': 'Имя должно быть не более 30 символов!',
        'bad_phone': 'Некорректный номер телефона "{value}"!',
        'bad_email': 'Некорректный eMail "{value}"!',
        'bad_fullname': 'Некорректный полное имя (ФИО)!',
        'phone_ex': 'Такой телефон "{value}" уже есть!',
        'phone_no': 'Телефон "{value}" не найден!',
        'email_ex': 'Такой Email "{value}" уже есть!',
        'email_no': 'Email "{value}" не найден!',
        'com_cancel': "Команда отменена.",
        'bad_key_com': 'Недопустимый ключ --{key} для команды {command}',
        'bad_command': 'Команда "{command}" не определена для AddressBook.',
        'record_ex': 'Такой контакт "{vname}" уже есть!',
        'record_no': 'Контакт "{vname}" не найден!',
        'con_list': 'Список контактов',
        'bd_list': "Список контактов, у которых день рождения в ближайшие {days} дней",
        'bd_no': "Отсутствуют контакты у которых день рождения в ближайшие {days} дней.",
        'bd_days': "(до дня рождения {dtb} дней)",
        'bad_command': 'Неизвестная команда "{command}".',
        'maybe_meant': " Возможно вы имели в виду: {maybe}.",
        'hello': 'Привет!\nЧем я могу вам помочь?',
        'good_bye': 'До свидания!',
        'dest_folder': "Введите путь, куда сортировать (по умолчанию в ту же папку):"
    },
    'uk': {
        'name_req': "Ім'я обов'язкове!",
        'name_30': "Ім'я має містити не більше 30 символів!",
        'bad_phone': 'Некоректний номер телефону "{value}"!',
        'bad_email': 'Некоректний eMail "{value}"!',
        'bad_fullname': "Некоректне повне ім'я (ПІБ)!",
        'phone_ex': 'Такий телефон "{value}" вже є!',
        'phone_no': 'Телефон "{value}" не знайдений!',
        'email_ex': 'Такий Email "{value}" вже є!',
        'email_no': 'Email "{value}" не знайдений!',
        'com_cancel': "Команда відмінена.",
        'bad_key_com': 'Неприпустимий ключ --{key} для команди {command}',
        'bad_command': 'Команда "{command}" не визначена для AddressBook.',
        'record_ex': 'Такий контакт "{vname}" вже є!',
        'record_no': 'Контакт "{vname}" не знайдений!',
        'con_list': 'Список контактів',
        'bd_list': "Список контактів, у яких день народження в найближчі {days} днів",
        'bd_no': "Відсутні контакти у яких день народження в найближчі {days} днів.",
        'bd_days': "(до дня народження {dtb} днів)",
        'bad_command': 'Невідома команда "{command}".',
        'maybe_meant': " Можливо ви мали на увазі: {maybe}.",
        'hello': 'Привіт!\nЧим я можу вам допомогти?',
        'good_bye': 'До побачення!',
        'dest_folder': "Введіть шлях, куди сортувати (за замовчуванням сортування в ту ж папку):"
    }
}

def get_message(key: str):
    res = messages[get_language()].get(key)
    return res if res else key

########################################## Base Classes ############################################

# буде батьківським для всіх полів
class Field:

    _value = None
    
    def __init__(self, value):
        self._value = value
        # self.value = value

    def _get_value(self):
        return self._value
    
    def _check_value(self, value):
        return value
    
    @property
    def value(self):
        return self._get_value()

    @value.setter
    def value(self, value):
        self._value = self._check_value(value)

    def is_search(self, mask: str):
        msk = mask.lower()
        st = str(self).lower()
        return st.find(msk) >= 0

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)
        self.value = name.capitalize()

    def _check_value(self, value):
        if not value:
            raise ValueError(get_message('name_req'))
        elif len(value) > 30:
            raise ValueError(get_message('name_30'))
        return value
    

# необов'язкове поле з телефоном та таких один запис (Record) може містити кілька
class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)
        self.value = phone

    def _get_value(self):
        return format_phone_number(self._value)
    
    def _check_value(self, value):
        ph = sanitize_phone_number(value)
        if re.match(r"(\b\d{10}\b)|(\+?\d{11}\b)|(\+?\d{12}\b)", ph):
            self._value = ph
        else:
            raise ValueError(get_message('bad_phone').replace("{value}",value)) 
        return ph
    

class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)
        self.value = birthday

    def _get_value(self):
        return '' if not self._value else self._value.strftime('%Y-%m-%d')
    
    def _check_value(self, value):
        return None if not value else get_date(value)
    

class Address(Field):
    def __init__(self, address):
        super().__init__(address)
        self.value = address

    def _get_value(self):
        return '' if not self._value else self._value
    
    def _check_value(self, value):
        return  None if not value else self.value
    

class Email(Field):
    def __init__(self, email):
        super().__init__(email)
        self.value = email

    def _get_value(self):
        return '' if not self._value else self._value
    
    def _check_value(self, value):
        if not value:
            return None
        elif re.findall(r'(^[a-zA-Z]{1,}[a-zA-Z0-9_.]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,}$)', value):
            return value
        else:
            raise ValueError(get_message('bad_email').replace("{value}", value))
    

class FullName(Field):
    def __init__(self, full_name):
        super().__init__(full_name)
        self.value = full_name

    def _get_value(self):
        return '' if not self._value else self._value
    
    def _check_value(self, value):
        if not value:
            return None
        elif re.match(r'(^[a-zA-Z\s\-]{2,}$)', value):
            return value
        else:
            raise ValueError(get_message('bad_fullname'))
   

#---------------------------------------------------------------------------------------------------

class ValueList(UserList):
    def __init__(self, value: Field | str =None):
        super().__init__()
        if isinstance(value, Field):
            self.append(value)
        elif value: 
            val_list = value.split(',')
            for item in val_list:
                self.append(item)
        self.iter_index = 0

    def is_search(self, mask: str):
        if self.data:
            for val in self:
                if val.is_search(mask):
                    return True
        return False

    def __repr__(self):
        return ', '.join(map(str, self))

    def __str__(self):
        return ', '.join(map(str, self))

    def __iter__(self):
        self.iter_index = 0
        return self
    
    def __next__(self):
        if self.iter_index >= len(self):
            self.iter_index = 0
            raise StopIteration
        else:
            res = self[self.iter_index]
            self.iter_index += 1
            return res

    def _get_message(self, key, value):
        if key == 'value_no':
            return 'Value {value} not found!'.replace('{value}', value)
        if key == 'value_ex':
            return 'Value {value} alredy exists!'.replace('{value}', value)
        return 'Incorrect value {value}!'.replace(' {value}', value)

    def _create_element(self, values):
        ps = values if isinstance(values, Field) else Field(values)
        return ps
    
    def exists(self, values, is_raise = None):
        """Search for a element by value
        
        is_raise = None - errors are not generated
                 = 1 - error if element exists
                 = -1 - error if element does not exist
        """
        val = values.value if isinstance(values, Field) else self._create_element(values).value
        for i in range(len(self)):
            ps = self[i]
            if ps.value == val:
                if is_raise == 1:
                    raise ValueError(self._get_message('value_ex', val))
                return ps
        if is_raise == -1:
            raise ValueError(self._get_message('value_no', val))
        return None

    def append(self, values):
        """Adding one element to the self list
        
        The 'values' parameter can be of type descendant Field or a string.
        """
        if isinstance(values, Field):
            self.exists(values, is_raise = 1)
            self.data.append(values)
        elif len(values) > 0:
            self.exists(values, is_raise = 1)
            ps = self._create_element(values)
            self.data.append(ps)
            return ps
        return None

    def update(self, values, values_new):
        """Changing the element values in self with a new values
        
        The 'values' and 'values_new' parameters can be of type descendant Field or a string.
        If the returned object is no longer needed, it can be deleted.
        """
        ps = self.exists(values, is_raise = -1)
        self.exists(values_new, is_raise = 1)
        ps.value = values_new if not isinstance(values_new, Field) else values_new.value
        return ps

    def delete(self, values):
        """Removing one phone from the self.phones list
        
        The 'phone' parameter can be of type Phone or a string.
        If the returned object is no longer needed, it can be deleted.
        """
        ps = self.exists(values, is_raise = -1)
        self.data.remove(ps)
        return ps


class Phones(ValueList):
    def _get_message(self, key, value):
        _errors = {
            'value_no': 'phone_no',
            'value_ex': 'phone_ex',
            'bad_value': 'bad_phone'
        }
        ekey = _errors.get(key)
        return get_message(ekey).replace('{value}', value)

    def _create_element(self, values):
        ps = values if isinstance(values, Phone) else Phone(values)
        return ps


class Emails(ValueList):
    def _get_message(self, key, value):
        _errors = {
            'value_no': 'email_no',
            'value_ex': 'email_ex',
            'bad_value': 'bad_email'
        }
        ekey = _errors.get(key)
        return get_message(ekey).replace('{value}', value)

    def _create_element(self, values):
        ps = values if isinstance(values, Email) else Email(values)
        return ps


############################################# Record ###############################################

# відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
class Record:
    """Single Contact Record"""

    def __init__(self, interface, name, phone=None, birthday=None, email=None, fullname=None, address=None):
        self.interface = interface
        self.botsetting = Bot_setting(interface)
        self.name = name if type(name) == Name else Name(name)

        if type(phone) == Phones:
            self.phones = phone
        elif phone:
            self.phones = Phones(phone)
        else:
            self.phones = Phones()

        if type(email) == Emails:
            self.emails = email
        elif email:
            self.emails = Emails(email)
        else:
            self.emails = Emails()

        self.birthday = birthday if type(birthday) == Birthday else Birthday(birthday)
        self.full_name = fullname if type(fullname) == FullName else FullName(fullname)
        self.address = address if type(address) == Address else Address(address)

    def edit(self, phone=None, birthday=None, email=None, fullname=None, address=None):
        if phone:
            if type(phone) != Phones:
                phone = Phones(phone)
            self.phones.clear()
            self.phones.extend(phone)

        if email:
            if type(email) != Emails:
                email = Emails(email)
            self.emails.clear()
            self.emails.extend(email)

        if birthday:
            self.birthday.value = birthday.value if type(birthday) == Birthday else Birthday(birthday).value

        if fullname:
            self.full_name.value = fullname.value if type(fullname) == FullName else FullName(fullname).value

        if address:
            self.address.value = address.value if type(address) == Address else Address(address).value

    """
    Contact: <name>
    Birthday: <birthday> (до дня рождения X дней)'bd_days'
    Phones: <phone-1>, . . . , <phone-N>
    eMails: <email-1>, . . . , <email-K>
    Full Name: <full_name>
    Address: <address>
    """
    def view_record(self, sep_top=False, sep_bottom=False):
        """Get a list of phones in one line from self.phones"""
        res = sep + '\n' if sep_top else '' 
        res = res + 'Contact: ' + self.name.value
        
        if self.birthday.value:
            dtb = self.days_to_birthday()
            sdtb = get_message('bd_days').replace('{dtb}', str(dtb))
            res = res + '\nBirthday: ' + self.birthday.value + ' ' + sdtb
        
        if any(self.phones):
            res = res + '\nPhones: ' + ', '.join(map(str, self.phones))

        if any(self.emails):
            res = res + ' \neMails: ' + ', '.join(map(str, self.emails))
        
        if self.full_name.value:
            res = res + '\nFull Name: ' + self.full_name.value
        
        if self.address.value:
            res = res + '\nAddress: ' + self.address.value
        
        if sep_bottom:
            res = res + '\n' + sep
        return res
    
    def is_search(self, mask: str):
        if self.name.is_search(mask):
            return True
        if self.birthday.value and self.birthday.is_search(mask):
            return True
        # if any(self.phones):
        #     for rec in self.phones:
        #         if rec.is_search(mask):
        #             return True
        if self.phones.is_search(mask):
            return True
        # if any(self.emails):
        #     for rec in self.emails:
        #         if rec.is_search(mask):
        #             return True
        if self.emails.is_search(mask):
            return True
        if self.full_name.value and self.full_name.is_search(mask):
            return True
        if self.address.value and self.birthday.is_search(mask):
            return True
        return False

    # def birthday_save(self, birthday):
    #     """Saving the birthday in self.birthday"""
    #     self.birthday.value = birthday.value if type(birthday) == Birthday else birthday

    # def address_save(self, address):
    #     """Saving the address in self.address"""
    #     self.address.value = address.value if type(address) == Address else address

    # def fullname_save(self, fullname):
    #     """Saving the fullname in self.fullname"""
    #     self.full_name.value = fullname.value if type(fullname) == FullName else fullname

    def days_to_birthday(self):     # повертає кількість днів до наступного дня народження
        if self.birthday.value:
            cdt = datetime.now().date()
            dt = datetime.strptime(self.birthday.value, '%Y-%m-%d')
            dt = date(cdt.year, dt.month, dt.day)
            if dt < cdt:
                dt = date(cdt.year + 1, dt.month, dt.day)
            rdt = (dt - cdt)
            return int(rdt.days)
        return None

    def __repr__(self):
        return self.view_record()

    def to_json(self):
        res = {'name': str(self.name),
               'phones': [{'value': str(phone)} for phone in self.phones],
               'birthday': self.birthday.value,
               'emails': [{'value': str(email)} for email in self.emails],
               'full_name': self.full_name.value,
               'address': self.address.value
              }
        return res

    def from_json(self, record_data):
        phones_data = record_data["phones"]
        for phone_data in phones_data:
            phone = phone_data["value"]
            if not self.phones.exists(phone):
                self.phones.append(phone)

        birthday = record_data.get('birthday')
        if birthday:
            self.birthday.value = birthday

        emails_data = record_data.get("emails")
        if emails_data:
            for email_data in emails_data:
                email = email_data["value"]
                if not self.emails.exists(email):
                    self.emails.append(email)

        full_name = record_data.get('full_name')
        if full_name:
            self.full_name.value = full_name

        address = record_data.get('address')
        if address:
            self.address.value = address

    # ------------------------------------------------------------------------------------
    
    fields = ['Name', 'Phone', 'Birthday', 'eMail', 'FullName', 'Address']

    def action_add(self, key, list_params):
        max_param = 5 if key == 'contact' else 1
        index = 1
        while True:
            try:
                ekey = self.fields[index].lower() if key == 'contact' else key
                val = self.botsetting.get_param(list_params, index, self.fields[index], required=0)
                if ekey == 'phone':
                    self.phones.append(val)
                elif ekey == 'birthday':
                    self.birthday.value = val
                elif ekey == 'email':
                    self.emails.append(val)
                elif ekey == 'fullname':
                    self.full_name.value = val
                elif ekey == 'address':
                    self.address.value = val
                index += 1
                if index > max_param:
                    break
            except ValueError as e:
                self.interface.print(str(e))
            except CommandCancel:
                break
            except Exception as e:
                return str(e)
        return 'Ok'

    def action_edit(self, key, list_params):
        val = self.botsetting.get_param(list_params, 1, self.fields[1], required=0)
        if key == 'contact':
            newphone = None
            newbirthday = None
            newmail = None
            newfullname = None
            newaddress = None
            max_param = 5
            index = 1
            while True:
                try:
                    if index == 1:
                        newphone = Phone(val)
                    elif index == 2:
                        newbirthday = Birthday(val)
                    elif index == 3:
                        newmail = Email(val)
                    elif index == 4:
                        newfullname = FullName(val)
                    elif index == 5:
                        newaddress = Address(val)
                    index += 1
                    if index > max_param:
                        break
                    val = self.botsetting.get_param(list_params, index, self.fields[index], required=0)
                except ValueError as e:
                    self.interface.print(str(e))
                except CommandCancel:
                    break
                except Exception as e:
                    return str(e)

            self.edit(newphone, newbirthday, newmail, newfullname, newaddress)
                    
        elif key in ('phone','email'):
            newval = self.botsetting.get_param(list_params, index, self.fields[2], required=1)
            if val:
                if key == 'phone':
                    self.phones.update(val, newval)
                else:
                    self.emails.update(val, newval)
            else:
                if key == 'phone':
                    newphone = Phone(newval)
                    self.phones.clear()
                    self.phones.append(newphone)
                else:
                    newmail = Email(newval)
                    self.emails.clear()
                    self.emails.append(newmail)
                    
        elif key == 'birthday':
            self.birthday.value = val
        elif key == 'fullname':
            self.full_name.value = val
        elif key == 'address':
            self.address.value = val
        return 'Ok'

    def action_del(self, key, list_params):
        if key == 'phone':
            val = self.botsetting.get_param(list_params, 1, self.fields[1], required=1)
            self.phones.delete(val)
        elif key == 'email':
            val = self.botsetting.get_param(list_params, 1, self.fields[3], required=1)
            self.emails.delete(val)
        return 'Ok'

########################################## AddressBook #############################################

class AddressBook(UserDict):
    """Contact book"""

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.botsetting = Bot_setting(interface)

    def fn_add(self, key, list_params):
        name = self.botsetting.get_param(list_params, 0, 'Contact Name', 1)
        if key == 'contact':
            rec = self.rec_add(name)
        else:
            rec = self.record_exists(name, is_raise = -1)
        res = rec.action_add(key, list_params)
        return res

    def fn_change(self, key, list_params):
        name = self.botsetting.get_param(list_params, 0, 'Contact Name', 1)
        rec = self.record_exists(name, is_raise = -1)
        res = rec.action_edit(key, list_params)
        return res
        
    def fn_delete(self, key, list_params):
        name = self.botsetting.get_param(list_params, 0, 'Contact Name', 1)
        rec = self.record_exists(name, is_raise = -1)
        if key == 'contact':
            self.rec_delete(name)
            res = 'Ok'
        else:
            res = rec.action_del(key, list_params)
        return res
    
    def fn_search(self, key, list_params):
        mask = self.botsetting.get_param(list_params, 0, 'Substring', 1)
        res = self.search_records(mask)
        return res
    
    def fun_show(self, key='contact', list_params=[]):
        if key == 'contact':
            if len(list_params) > 0:
                res = self.list_records(list_params[0])
                res = '\n'.join(res)
            else:
                res = self.interface.display_chunks(self.view_records)
        elif key == 'birthdays':
            if len(list_params) > 0 and str(list_params[0]).isdecimal():
                dtb = int(list_params[0])
            else:
                dtb = get_number_of_days()
            res = self.view_birthdays(dtb)
        else:
            res = get_message('bad_key_com').replace('{key}', key).replace('{command}', 'show')
        return res

    """
    Dictionary of valid commands.
    Key - команда.
    Value - функция выполнения команды.
    """
    funcs = {
        "add": fn_add,
        "change": fn_change,
        "delete": fn_delete,
        #
        "search": fn_search,
        "show": fun_show
    }

    def action(self, command, key, list_params):
        fcom = self.funcs.get(command)              # функция выполнения команды.
        if fcom is None:
            res =  get_message('bad_command').replace('{command}', command)
        else:
            res = fcom(self, key, list_params)
        return res


    def record_exists(self, rec_name, is_raise=None):
        """Search for a contact by name
        
        is_raise = None - errors are not generated
                 = 1 - error if record exists
                 = -1 - error if record does not exist
        """
        if type(rec_name) == Record:
            vname = rec_name.name.value
        else:
            vname = rec_name.value if type(rec_name) == Name else Name(rec_name).value
        if len(self.data) > 0:
            for key, rec in self.data.items():
                if key == vname:
                    if is_raise == 1:
                        raise Exception(get_message('record_ex').replace('{vname}', vname))
                    return rec
            if is_raise == -1:
                raise Exception(get_message('record_no').replace('{vname}', vname))
        return None

    def add_record(self, record: Record):
        """Adding a contact by record"""
        self.rec_add(record, record.phones, record.birthday, record.emails, record.full_name, record.address)

    def rec_add(self, rec_name, phone=None, birthday=None, email=None, fullname=None, address=None):
        """Adding a contact by name
        
        If the returned object is no longer needed, it can be deleted.
        """
        if type(rec_name) == Record:
            vname = rec_name.name.value
        else:
            vname = rec_name.value if type(rec_name) == Name else Name(rec_name).value
        self.record_exists(vname, is_raise = 1)
        rec = rec_name if type(rec_name) == Record else Record(self.interface, rec_name)
        self.data.update({vname: rec})
        rec.edit(phone, birthday, email, fullname, address)
        return rec

    def update_record(self, record: Record):
        """Edit a contact by record"""
        self.rec_update(record, record.phones, record.birthday, record.emails, record.full_name, record.address)

    def rec_update(self, rec_name, phone=None, birthday=None, email=None, fullname=None, address=None):
        """Edit a contact by name"""
        rec = self.record_exists(rec_name, is_raise = -1)
        rec.edit(phone, birthday, email, fullname, address)

    def delete_record(self, record):
        """Deleting a contact by record"""
        self.rec_delete(record.name.value)

    def rec_delete(self, rec_name):
        """Deleting a contact by name
        
        If the returned object is no longer needed, it can be deleted.
        """
        rec = self.record_exists(rec_name, is_raise = -1)
        self.pop(rec.name.value)
        # if type(rec_name) != Record:
        #     del rec
        return rec
    
    def list_records(self, name=''):
        """Getting a list of all contacts"""
        res = []
        vname = name.value if type(name) == Name else name
        if len(vname) > 0:
            vname = Name(name).value
            res.append(self.record_exists(vname, is_raise = -1).view_record(sep_top=True, sep_bottom=True))
        else:
            s_top = True
            for key, rec in self.data.items():
                res.append(rec.view_record(sep_top=s_top, sep_bottom=True))
                s_top = False
        return res

    def phone_add(self, name, phone):
        """Adding a phone number to an existing contact in self.phones"""
        rec = self.record_exists(name, is_raise = -1)
        rec.phones.append(phone)

    def phone_correct(self, name, phone, phone_new):
        """Changing the phone number in self.phones with a new number"""
        rec = self.record_exists(name, is_raise = -1)
        rec.phones.update(phone, phone_new)

    def phone_delete(self, name, phone):
        """Deleting a phone number from an existing contact in self.phones"""
        rec = self.record_exists(name, is_raise = -1)
        ps = rec.phones.delete(phone)
        return ps

    def email_add(self, name, email):
        """Adding a email number to an existing contact in self.emails"""
        rec = self.record_exists(name, is_raise = -1)
        rec.phones.append(email)

    def email_correct(self, name, email, email_new):
        """Changing the email in self.phones with a new email"""
        rec = self.record_exists(name, is_raise = -1)
        rec.emails.update(email, email_new)

    def email_delete(self, name, email):
        """Deleting a email from an existing contact in self.emails"""
        rec = self.record_exists(name, is_raise = -1)
        ps = rec.phones.delete(email)
        return ps

    def birthday_save(self, name, birthday):
        """Saving the birthday in self.birthday"""
        rec = self.record_exists(name, is_raise = -1)
        rec.birthday.value = birthday

    def fullname_save(self, name, birthday):
        """Saving the birthday in self.birthday"""
        rec = self.record_exists(name, is_raise = -1)
        rec.full_name.value = birthday

    def address_save(self, name, birthday):
        """Saving the birthday in self.birthday"""
        rec = self.record_exists(name, is_raise = -1)
        rec.address.value = birthday

    def search_records(self, mask):
        """Search for contacts by fragment of name or by fragment of phone number"""
        head = get_message('con_list') + ' (search):\n'
        res = ''
        for key, rec in self.data.items():
            if rec.is_search(mask):
                st = rec.view_record(sep_bottom=True)
                res = res + '\n' + st
        if len(res) == 0:
            res = head + sep + '\n' + sep
        else:
            res = head + sep + res
        return res

    def view_records(self, chunk_size = get_display_lines()):
        """
        Display the entire address book in chunks of chunk_size entries.

        If chunk_size == None or 0, then all records are displayed in one chunk.
        """
        _chunk_num = 0
        _chunk_size = int(chunk_size)
        head = get_message('con_list') + ':'
        res = head
        _index = 1
        try:
            for key, rec in self.data.items():
                s_top = (_index == 1)
                txt = rec.view_record(sep_top=s_top, sep_bottom=True)
                _index = _index + txt.count('\n') + 1
                res = res  + '\n' + txt
                if (_chunk_size > 0) and (_index // _chunk_size != _chunk_num):
                    yield res
                    _chunk_num += 1
                    res = ''
            if _index == 1:
                res = res +'\n' + sep +'\n' + sep
            if len(res) > 0:
                yield res
        except Exception as e:
            self.interface.print(str(e))
        finally:
            return 

    def view_birthdays(self, days = get_number_of_days):
        head =  get_message('bd_list').replace('{days}', str(days))
        res = ''
        for record in self.data.values():
            if record.birthday.value:
                dtb = int(record.days_to_birthday())
                if dtb <= int(days):
                    res += record.view_record(sep_bottom=True) + "\n"
        if res:
            return head + '\n' + sep + '\n' + res.rstrip()
        return  get_message('bd_no').replace('{days}', str(days))

    def __repr__(self):
        for res in self.view_records(0):
            pass
        return res

    def __str__(self):
        for res in self.view_records(0):
            pass
        return res

    # ------------------------------------------------------------------------------------

    def to_json(self):
        result = []
        for name, record in self.data.items():
            result.append(record.to_json())
        return result

    def save_json(self, filename):
        file_path = pathlib.Path(os.path.dirname(filename))
        if not file_path.exists():
            file_path.mkdir(parents=True)

        data = {'records': self.to_json()}
        with open(filename, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_json(self, filename):
        file_path = pathlib.Path(filename)
        if not file_path.exists():
            return False
        with open(filename, 'r') as file:
            data = json.load(file)
            records = data["records"]
            self.from_json(records)
        return True

    def from_json(self, records_json):
        for record_data in records_json:
            name = record_data['name']
            record = self.record_exists(name)
            if not record:
                record = Record(self.interface, name)
                self.add_record(record)
            
            record.from_json(record_data)

##########################################################################################

if __name__ == '__main__':
    from userinterface import ConsoleInterface
    ui = ConsoleInterface()

    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(ui, name, phone)
    rec.phones.append('0501234567')
    rec.birthday.value = '29.04.1999'
    ab = AddressBook(ui)
    ab.add_record(rec)
    ab.rec_add('Dany','380634567890,+380990123456','2001/11/21')
    # assert isinstance(ab['Bill'], Record)
    # assert isinstance(ab['Bill'].name, Name)
    # assert isinstance(ab['Bill'].phones, UserList)
    # assert isinstance(ab['Bill'].phones[0], Phone)
    # assert ab['Bill'].phones[0].value == '123-456-7890'
    # assert ab['Bill'].phones[1].value == '+38(050)123-4567'
    # assert isinstance(ab['Bill'].birthday, Birthday)
    # assert ab['Bill'].birthday.value == '1999-04-29'
    # assert isinstance(ab['Dany'].phones[0], Phone)
    # assert ab['Dany'].phones[0].value == '+38(063)456-7890'
    # assert ab['Dany'].phones[1].value == '+38(099)012-3456'
    # assert isinstance(ab['Dany'].birthday, Birthday)
    # assert ab['Dany'].birthday.value == '2001-11-21'
    print(ab['Dany'])
    print(ab)
    # # print('All Ok')

    # # book = AddressBook()
    # book = ab
    # book.rec_add('Yurii', '+38(067)576-1490, +38(050)031-7201')
    # # # print(book.list_records())

    # book.rec_add('My', '+1(250)241-7847')
    # # # print(book.list_records())

    # book.rec_add('Maryna', '+38(095)001-6123')
    # # # print(book.list_records())
    # # # print(book.list_records('My'))
    # print(book)

    # book.rec_delete('My')
    # print(book)

    # book.rec_update('Yurii', '+38(067)576-1490, +38(050)031-7201, +1(250)241-7845')
    # print(book)

    # book['Yurii'].phone_correct('+1(250)241-7845', '+1(250)241-7847')
    # print(book.list_records())
    # print(book['Yurii'])
    
    # # ls = ''
    # # for txt in book.view_records(2):
    # #     if len(ls) == 0:
    # #         ls = txt
    # #     else:
    # #         print(ls)
    # #         if input('') == '/q':
    # #             ls = ''
    # #             break
    # #         ls = txt
    # # if len(ls) > 0:
    # #     print(ls)

    # phones = Phones('+38(067)576-1490, +38(050)031-7201, +1(250)241-7847')
    # print(phones)

    # # for ph in phones:     # Test Iterable
    # #     print(ph)
    # #     break
    # # print(phones)
    # # for ph in phones:
    # #     print(ph)

    # ind = phones.index('+38(050)031-7201')
    # print(str(ind))     # Test Index => succes
    # try:
    #     ind = phones.index('+38(050)031-7200')
    #     print(str(ind)) # Test Index => eroor
    # except Exception as e:
    #     print(e)

    # try:
    #     phones[5] = '+38(050)031-7201'      # Test __setitem__ => eroor
    # except Exception as e:
    #     print(e)

    # phones[5] = '+38(050)031-7200'           # Test __setitem__ => succes
    # print(phones)

    # print(phones[2])        # Test __getitem__
    # print(phones[5])        # Test __getitem__

    # phones.append('+38(095)001-6123')
    # print(phones)
    # try:
    #     phones.append('+38(095)001-6123')
    # except Exception as e:
    #     print(e)

    # phones.remove('+38(050)031-7200')       # Test remove => succes
    # print(phones)
    # try:
    #     phones.remove('+38(050)031-7200')   # Test remove => eroor
    # except Exception as e:
    #     print(e)

    # phone = Phone('1234567890')
    # vl = ValueList(phone)
    # print(vl)

    # vl.append(Phone('+38(050)031-7200'))
    # print(vl)

    # vl = Phones('+38(067)576-1490, +38(050)031-7201, +12502417847')
    # print(vl)
