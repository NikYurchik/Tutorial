from collections import UserList, UserDict, UserString

"""
Користувач взаємодіє з книгой контактів (AddressBook), додаючи, видаляючи та редагуючи записи (Record).
Також користувач повинен мати можливість шукати в книзі контактів записи за одному або декількома критеріями (полям).
Записи Record у AddressBook зберігаються як значення у словнику. В якості ключів використовується значення Record.name.value.

Record зберігає об'єкт Name в окремому атрибуті.
Record зберігає список об'єктів Phone в окремому атрибуті.
Record реалізує методи для додавання/видалення/редагування об'єктів Phone.

Поля (Field) можуть бути обов'язковими (ім'я) та необов'язковими (телефон або email наприклад).
Записи можуть містити декілька полів одного типу (декілька телефонів наприклад).
Користувач повинен мати можливість додавати/видаляти/редагувати поля у будь-якому записі.
"""

# буде батьківським для всіх полів
class Field:
    value = ''
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass

# необов'язкове поле з телефоном та таких один запис (Record) може містити кілька
class Phone(Field):
    pass

# class Email(Field):
#     pass

# відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
class Record:
    """Single Contact Record"""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = UserList()
        #self.emails = UserList()

    def phone_add(self, *phone):
        """Adding phones to the self.phones list"""
        for phone2 in phone:
            if type(phone2) == type(()):
                for ph in phone2:
                    self.phones.append(Phone(ph))
            else:
                self.phones.append(Phone(phone2))

    def phone_update(self, *phone):
        """Changing the list of phones in self.phones with a new list"""
        self.phones.clear()
        for phone2 in phone:
            if type(phone2) == type(()):
                for ph in phone2:
                    self.phone_add(ph)
            else:
                self.phone_add(phone2)

    def phone_correct(self, phone, phone_new):
        """Changing the phone number in self.phones with a new number"""
        for i in range(len(self.phones)):
            ps = self.phones[i]
            if ps.value == phone:
                ps.value = phone_new
                break

    def phone_delete(self, *phone):
        """Removing phones from the self.phones list"""
        def _delete(phone):
            for i in range(len(self.phones)):
                ps = self.phones[i]
                if ps.value == phone:
                    self.phones.remove(ps)
                    break
        #
        for phone2 in phone:
            if type(phone2) == type(()):
                for ph in phone2:
                    _delete(ph)
            else:
                _delete(phone2)

    def view_phones(self):
        """Get a list of phones in one line from self.phones"""
        st = ' '
        res = self.name.value + ':'
        for ph in self.phones.data:
            res = res + st + ph.value
            st = ', '
        return res
        
    # def email_add(self, *email):
    #     pass

    # def email_update(self, *email):
    #     pass

    # def email_delete(self, *email):
    #     pass


class AddressBook(UserDict):
    """Contact book"""

    def record_exists(self, name):
        """Search for a contact by name"""
        if len(self.data) > 0:
            for key, rec in self.data.items():
                if key == name:
                    return rec
        return None

    def record_add(self, name, *record):
        """Adding a contact by name"""
        rec = self.record_exists(name)
        if rec == None:
            rec = Record(name)
            if len(record) > 0:
                for tel in record:
                    rec.phone_add(tel)
            self.update({name: rec})
        else:
            raise ValueError('Record "{name}" alredy exists!')

    def record_update(self, name, *record):
        """Edit a contact by name"""
        rec = self.record_exists(name)
        if rec == None:
            raise ValueError('Record "{name}" not found!')
        else:
            rec.phone_update(record)

    def record_delete(self, name):
        """Deleting a contact by name"""
        rec = self.record_exists(name)
        if rec == None:
            raise ValueError('Record "{name}" not found!')
        else:
            self.pop(name)
    
    def view_records(self, name=''):
        """Getting a list of all contacts"""
        res = []
        if len(name) > 0:
            res.append(self.record_exists(name).view_phones())
        else:
            for key, rec in self.data.items():
                res.append(rec.view_phones())
        return res


book = AddressBook()
book.record_add('Yurii', '+38(067)576-1490', '+38(050)031-7201')
print(book.view_records())

book.record_add('My', '+1(250)241-7847')
print(book.view_records())

book.record_add('Maryna', '+38(095)001-6123')
print(book.view_records())
print(book.view_records('My'))

book.record_delete('My')
print(book.view_records())

book.record_update('Yurii', '+38(067)576-1490', '+38(050)031-7201', '+1(250)241-7847')
print(book.view_records())
