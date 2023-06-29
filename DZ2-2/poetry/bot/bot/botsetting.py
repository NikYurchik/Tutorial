import os
import pathlib
import json
from userinterface import ConsoleInterface

request_details = 1  # запрашивать ли в командном режиме недостающие реквизиты контакта;
display_birthdays = 0  # выводить ли при запуске бота список контактов, у которых день рождения попадает в заданный период от текущего дня;
number_of_days = 7  # количество дней от текущего дня для вывода списка контактов, у которых день рождения приходится на этот период.
display_lines = 10  # количество отображаемых строк в одной порции вывода списка контактов или заметок
language = "ru" # язык интерфейса (en - English, ru - русский, uk - український)

def get_request_details():
    return str(request_details)

def get_display_birthdays():
    return str(display_birthdays)

def get_number_of_days():
    return str(number_of_days)

def get_display_lines():
    return str(display_lines)

def get_language():
    return language


class CommandCancel(Exception):
    pass

class Bot_setting:
    __instance = None

    def __new__(cls, start_value: int = 0, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance


    setting_lang = {}
    errors = {}

    # def get_request_details(self):
    #     return str(request_details)

    # def get_display_birthdays(self):
    #     return str(display_birthdays)

    # def get_number_of_days(self):
    #     return str(number_of_days)

    # def get_display_lines(self):
    #     return str(display_lines)

    # def get_language(self):
    #     return language

    setting_dict = {
        'en': {
            'header': [
                "Bot settins.",
                '',
                None
            ],
            'request_details': [
                "Whether to request missing contact details in command mode (1 - yes, 0 - no).",
                get_request_details
            ],
            'display_birthdays': [
                "Should the bot launch a list of contacts whose birthday falls within a specified period from the current day (1 - yes, 0 - no).",
                get_display_birthdays
            ],
            'number_of_days': [
                "Number of days from the current day to display a list of contacts whose birthday falls within this period.",
                get_number_of_days
            ],
            'display_lines': [
                "The number of rows to display in one portion of the output list of contacts or notes.",
                get_display_lines
            ],
            'language': [
                "Interface language (en - English, ru - Russian, uk - Ukrainian).",
                get_language
            ]
        },
        'ru': {
            'header': [
                "Настройки бота.",
                '',
                None
            ],
            'request_details': [
                "Запрашивать ли в командном режиме недостающие реквизиты контакта (1 - да, 0 - нет).",
                get_request_details
            ],
            'display_birthdays': [
                "Выводить ли при запуске бота список контактов, у которых день рождения попадает в заданный период от текущего дня (1 - да, 0 - нет).",
                get_display_birthdays
            ],
            'number_of_days': [
                "Количество дней от текущего дня для вывода списка контактов, у которых день рождения приходится на этот период.",
                get_number_of_days
            ],
            'display_lines': [
                "Количество отображаемых строк в одной порции вывода списка контактов или заметок.",
                get_display_lines
            ],
            'language': [
                "Язык интерфейса (en - English, ru - русский, uk - український).",
                get_language
            ]
        },
        'uk': {
            'header': [
                "Налаштування боту.",
                None
            ],
            'request_details': [
                "Чи вимагати в командному режимі реквізити контакту, якого не вистачає (1 - так, 0 - ні).",
                get_request_details
            ],
            'display_birthdays': [
                "Чи виводити при запуску бота список контактів, у яких день народження потрапляє у заданий період від поточного дня (1 - так, 0 - ні).",
                get_display_birthdays
            ],
            'number_of_days': [
                "Кількість днів від поточного дня для виведення списку контактів, у яких день народження припадає на цей період.",
                get_number_of_days
            ],
            'display_lines': [
                "Кількість рядків, що відображаються в одній порції виведення списку контактів або нотаток.",
                get_display_lines
            ],
            'language': [
                "Мова інтерфейсу (en - English, ru - російська, uk - українська).",
                get_language
            ]
        }
    }

    error_dict = {
        'en': {
            'bad_value': "Invalid value '{value}' for setting '{key}'",
            'bad_key': "Invalid setting key '{key}'",
            'com_cancel': "Command canceled",
            'enter_value': "value"
        },
        'ru': {
            'bad_value': "Недопустимое значение '{value}' для настройки '{key}'",
            'bad_key': "Недопустимый ключ настройки '{key}'",
            'com_cancel': "Команда отменена",
            'enter_value': 'значение'
        },
        'uk': {
            'bad_value': "Неприпустиме значення '{value}' для налаштування '{key}'",
            'bad_key': "Неприпустимий ключ налаштування '{key}'",
            'com_cancel': "Команда відмінена",
            'enter_value': 'значення'
        }
    }
    def __init__(self, interface):
        self.interface = interface
        self.init_language()

    def init_language(self):
        global language
        self.setting_lang = self.setting_dict.get(language)
        self.errors = self.error_dict.get(language)

    def set_request_details(self, value):
        global request_details
        if value not in ['0', '1']:
            raise Exception(self._errors['bad_value'].replace('{value}', value).replace('{key}', 'request_details'))
        request_details = int(value)

    def set_display_birthdays(self, value):
        global display_birthdays
        if value not in ['0', '1']:
            raise Exception(self._errors['bad_value'].replace('{value}', value).replace('{key}', 'display_birthdays'))
        display_birthdays = int(value)

    def set_number_of_days(self, value):
        global number_of_days
        if not str(value).isdecimal() or int(value) < 0 or int(value) > 365:
            raise Exception(self._errors['bad_value'].replace('{value}', value).replace('{key}', 'number_of_days'))
        number_of_days = int(value)

    def set_display_lines(self, value):
        global display_lines
        if not str(value).isdecimal() or int(value) < 0 or int(value) > 50:
            raise Exception(self._errors['bad_value'].replace('{value}', value).replace('{key}', 'display_lines'))
        display_lines = int(value)

    def set_language(self, value):
        global language
        if value not in self.error_dict:
            raise Exception(self._errors['bad_value'].replace('{value}', value).replace('{key}', 'language'))
        language = value
        self.init_language()

    def set_setting(self, command, key, list_params):
        value = self.get_param(list_params, 0, self.errors['enter_value'], 1)
        if key == 'request_details':
            self.set_request_details(value)
        elif key == 'display_birthdays':
            self.set_display_birthdays(value)
        elif key == 'number_of_days':
            self.set_number_of_days(value)
        elif key == 'display_lines':
            self.set_display_lines(value)
        elif key == 'language':
            self.set_language(value)
        else:
            raise Exception(self.errors['bad_key'].replace('{key}'))

    def view_setting(self, key=''):
        if key:
            lst = self.setting_lang.get(key)
            val = lst[1]()
            res = key + ' = ' + val + '  - ' + lst[0]
        else:
            res = ''
            sep = '----------------------------------------------------------------------------------------------------'
            for key, lst in self.setting_lang.items():
                if key == 'header':
                    res = lst[0] +'\n' + sep + '\n'
                else:
                    val = lst[1]()
                    res = res + key + ' = ' + val + '  - ' + lst[0] +'\n'
            res = res + sep
        return res

    def __repr__(self):
        return self.view_setting()

    def __str__(self):
        return self.view_setting()

    def __call__(self, command, key, params):
        return self.set_setting(command, key, params)

    invitation = {
        'en': "Enter",
        'ru': "Введите",
        'uk': "Введіть"
    }
    param_required = {
        'en':  "Parameter required",
        'ru': "Параметр обязателен",
        'uk': "Параметр обов'язковий"
    }
    com_cancel = {
        'en': "Command canceled.",
        'ru': "Команда отменена.",
        'uk': "Команда відмінена."
    }
    
    def get_param(self, list_params, index, description, required):
        if index < len(list_params):  # параметр есть в команде
            st = list_params[index]
        elif not required and not request_details:
            st = ''
        else:
            done = True
            while done:
                st = self.interface.input(f'{self.invitation[language]} {description} > ')
                if required and len(st) == 0:
                    self.interface.print(f'{self.param_required[language]}!')
                elif st == '/q':
                    raise CommandCancel(f'{self.com_cancel[language]}')
                else:
                    done = False
        return st


    def to_json(self):
        res = {'request_details': str(request_details),
               'display_birthdays': str(display_birthdays),
               'number_of_days': str(number_of_days),
               'display_lines': str(display_lines),
               'language': language
              }
        return res

    def from_json(self, record_data):
        request_details = record_data.get('request_details')
        if request_details:
            self.set_request_details(request_details)

        display_birthdays = record_data.get('display_birthdays')
        if display_birthdays:
            self.set_display_birthdays(display_birthdays)

        number_of_days = record_data.get('number_of_days')
        if number_of_days:
            self.set_number_of_days(number_of_days)

        display_lines = record_data.get('display_lines')
        if display_lines:
            self.set_display_lines(display_lines)

        language = record_data.get('language')
        if language:
            self.set_language(language)

    def save_json(self, filename):
        file_path = pathlib.Path(os.path.dirname(filename))
        if not file_path.exists():
            file_path.mkdir(parents=True)

        data = {'settings': self.to_json()}
        with open(filename, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_json(self, filename):
        file_path = pathlib.Path(filename)
        if not file_path.exists():
            return False
        
        with open(filename, 'r') as file:
            data = json.load(file)
            records = data["settings"]
            self.from_json(records)
        return True
        


if __name__ == '__main__':
    ui = ConsoleInterface()
    bh = Bot_setting(ui)
    # print (bh.setting_dict.get('en').get('request_details'))
    # print (bh.setting_dict.get('en').get('request_details')[1])
    print(bh)
    # print(bh.view_setting('request_details'))
    # bh.set_language('aa')
    bh.set_language('uk')
    print(bh.view_setting('request_details'))
    bh.set_language('en')
    print(bh.view_setting('request_details'))
