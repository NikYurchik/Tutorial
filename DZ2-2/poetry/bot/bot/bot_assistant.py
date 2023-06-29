import sys
import pathlib
import difflib

from virtual_assistant import AddressBook, get_message
from Notebook import NoteBook
# from sorter import Sorter
from bot_help import Bot_help
from botsetting import Bot_setting, get_display_birthdays, get_number_of_days
from bot_utils import split

home_directory = pathlib.Path.home().joinpath('bot_assistant', 'save')

class Bot_assistant:

    def __init__(self, interface) -> None:
        self.interface = interface
        self.home_directory = pathlib.Path.home().joinpath('bot_assistant', 'save')
        self.interactive_mode = 0
        self.addressbook = None  # адресная книга
        self.notebook = None  # книга заметок
        self.bothelp = None
        self.load_setting()
        self.com_key = ''

    def load_setting(self):
        self.botsetting = Bot_setting(self.interface)
        self.botsetting.load_json(f'{self.home_directory}/Setting.json')

    def check_addressbook(self):
        if self.addressbook is None:
            self.addressbook = AddressBook(self.interface)
            self.addressbook.load_json(f'{self.home_directory}/AddressBook.json')

    def check_notebook(self):
        if self.notebook is None:
            if self.notebook is None:
                self.notebook = NoteBook(self.interface)
                self.notebook.load_json(f'{self.home_directory}/NoteBook.json')

    def check_bothelp(self):
        if self.bothelp is None:
            self.bothelp = Bot_help(self.interface)


    def save_classes(self):
        self.save_setting()
        self.save_contacts()
        self.save_notebook()

    def save_contacts(self):
        if self.addressbook:
            self.addressbook.save_json(f'{self.home_directory}/AddressBook.json')

    def save_notebook(self):
        if self.notebook:
            self.notebook.save_json(f'{self.home_directory}/NoteBook.json')

    def save_setting(self):
        if self.botsetting:
            self.botsetting.save_json(f'{self.home_directory}/Setting.json')

    # --------------------------------------------------------------------------------

    def fun_hello(self, command, list_params):
        self.interactive_mode = 1
        res = get_message('hello')
        if get_display_birthdays():
            self.check_addressbook()
            res = self.addressbook.view_birthdays(get_number_of_days()) + '\n' + res
        return res

    def fun_exit(self, command, list_params):
        self.interactive_mode = 0
        return get_message('good_bye')

    # def func_sorter(self, command, list_params):
    #     sort = Sorter()
    #     destination = input(get_message('dest_folder'))
    #     sort.run(list_params, destination)
    #     return 'Ok'

    # --------------------------------------------------------------------------------

    def fn_help_action(self, command, key, params):
        self.check_bothelp()
        res = self.interface.display_help(self.bothelp, command, key, params)   # UserInterface
        return res

    def fn_contact_action(self, command, key, params):
        self.check_addressbook()
        if command in ('show','search'):
            res = self.interface.display_contacns(self.addressbook, command, key, params)   # UserInterface
        else:
            # res = self.addressbook.action(command, key, params)
            res = self.addressbook(command, key, params)
        return res

    def fn_note_action(self, command, key, params):
        self.check_notebook()
        if command in ('show','search'):
            res = self.interface.display_notes(self.notebook, command, key, params)     # UserInterface
        else:
            # res = self.notebook.action(command, key, params)
            res = self.notebook(command, key, params)
        return res

    def fn_setting_action(self, command, key, params):
        if command == 'show':
            ckey = '' if not params else params[0]
            return self.interface.display_setting(self.botsetting, command, ckey, params)   # UserInterface
        else:
            # self.botsetting.set_setting(command, key, params)
            self.botsetting(command, key, params)
        return 'Ok'

    def fn_save_action(self, command, key, params):
        if key == 'contacts':
            self.save_contacts()
        elif key == 'notes':
            self.save_notebook()
        elif key == 'setting':
            self.save_setting()
        else:
            self.save_classes()
        return 'Ok'

    def fn_sort_action(self, command, key, params):
        return 'Команда пока не реализована'        # sort --folder <source> [<target>]

    # --------------------------------------------------------------------------------

    def fun_action(self, command, params):
        """
        Предварительная обработка команды.

        Параметры:
        command - команда бота (см. словарь funcs)
        params - список: ключ и параметры команды (ключ и некоторые параметры могут отсутствовать).
        
        Выделяет ключ команды, проверяет корректность пары команда-ключ и вызывает
        процедуру обработки соответствующей подсистемы (AddressBook, NoteBook, Setting, Help).
        Возвращает строку с результатом выполнения обработчика соответствующей подсистемы.
        """
        cm = params
        lfn = self.funcs.get(command)
        if len(cm) > 0:  # есть параметры
            cm1 = cm[0]
            if cm1.startswith('--'):  # Есть ключ команды
                cm1 = cm1[2::]
                self.com_key = cm1
                cm.pop(0)  # убираем ключ команды
            else:
                cm1 = '--'
        else:
            cm1 = '--'

        if cm1 == '--':  # смотрим ключ по умолчанию
            cm1 = lfn[1]
            if len(cm1) > 0:  # есть ключ по умолчанию
                self.com_key = cm1

        cmk = self.keys.get(command)
        if cmk is None or self.com_key not in cmk.keys():
            res = get_message('bad_key_com').replace('{key}', cm1).replace('{command}', command)
            return res
        try:
            fn = cmk.get(self.com_key)
            res = fn(self, command, self.com_key, cm)     # команда, ключ и список параметров
        except Exception as e:
            res = str(e)
        return res


    # --------------------------------------------------------------------------------
    """
    Dictionary of valid commands.
    The key is the first word of the command.
    Value - list of command details:
    [0] - максимальное количество параметров комадды.
    [1] - ключ команды по умолчанию
    [2] - функция выполнения команды
    """
    funcs = {
        "hello": [0, '', fun_hello],
        "exit": [0, '', fun_exit],
        #
        "add": [6, 'contact', fun_action],
        "change": [6, 'contact', fun_action],
        "delete": [6, 'contact', fun_action],
        #
        "search": [1, 'contact', fun_action],
        "show": [1, 'contact', fun_action],
        #
        "help": [1, 'all', fun_action],
        "setting": [1, '', fun_action],
        "save": [1, 'all', fun_action],
        #
        "sort": [1, 'note', fun_action]
    }

    """
    Словарь командных ключей
    """
    keys = {
        "add":  {
                    'contact': fn_contact_action,
                    'phone': fn_contact_action,
                    'birthday': fn_contact_action,
                    'email': fn_contact_action,
                    'fullname': fn_contact_action,
                    'address': fn_contact_action,
                    'note': fn_note_action,
                    'tag': fn_note_action
                },
        "change":   {
                        'contact': fn_contact_action,
                        'phone': fn_contact_action,
                        'birthday': fn_contact_action,
                        'email': fn_contact_action,
                        'fullname': fn_contact_action,
                        'address': fn_contact_action,
                        'note': fn_note_action,
                        'tag': fn_note_action
                    },
        "delete":   {
                        'contact': fn_contact_action,
                        'phone': fn_contact_action,
                        'email': fn_contact_action,
                        'note': fn_note_action,
                        'tag': fn_note_action
                    },
        "search":   {
                        'contact': fn_contact_action,
                        'note': fn_note_action,
                        'tag': fn_note_action
                    },
        "show": {
                    'contact': fn_contact_action,
                    'birthdays': fn_contact_action,
                    'note': fn_note_action,
                    # 'tag': fn_note_action,
                    'setting': fn_setting_action
                },
        "help": {
                    'all': fn_help_action,
                    'note': fn_help_action
                },
        "setting":  {
                        'request_details': fn_setting_action,
                        'display_birthdays': fn_setting_action,
                        'number_of_days': fn_setting_action,
                        'display_lines': fn_setting_action,
                        'language': fn_setting_action
                    },
        "save": {
                    'all': fn_save_action,
                    'contacts': fn_save_action,
                    'notes': fn_save_action,
                    'setting': fn_save_action
                },
        "sort": {
                    'folder': fn_sort_action,
                    'note': fn_note_action,
                    'tag': fn_note_action
                }
    }

    def _closest_command(input_string, command_list):
        if input_string.lower() not in command_list:
            suggestion = difflib.get_close_matches(input_string, command_list, n=2, cutoff=0.55)
            res = get_message('un_command').replace('{command}', input_string)
            if suggestion:
                res = res + get_message('un_command').replace('{maybe_meant}', ', '.join(suggestion))
            return res

    def parcer(self, command):
        """ 
        Парсер команд бота 
        
        Принимаемая строка команды:
            <command> [--<key>] [<param-1> [... [param-N]...]]
        Распознаёт команду <command> и вызывает процедуру предварительной обработки команды.
        Возвращает строку с результатом выполнения обработчика.
        """
        res = ''
        if len(command) > 0:
            self.com_key = ''
            if type(command) == list:
                cm = command
            else:
                cm = split(command)
            cm0 = cm[0].lower()
            lfn = self.funcs.get(cm0)
            if lfn is None:
                res += '\n' + str(self._closest_command(cm0, self.funcs.keys()))
            else:
                cm.pop(0)  # убираем команду из списка

                try:
                    res = lfn[2](self, cm0, cm)     # команда и список параметров с ключем
                except Exception as e:
                    res = str(e)
        else:
            res = self.fun_hello('hello', [])       # Переход в интеактивный режим ввода команд
        return res


    def main(self):
        sys_argv = sys.argv
        command = []
        if len(sys_argv) > 1:
            for i in range(len(sys_argv)-1):
                command.append(sys_argv[i+1])
        while True:
            res = self.parcer(command)
            if res is not None:
                self.interface.print(res)
            if self.interactive_mode == 0:
                break
            cmd = self.interface.input('>> ')
            command = split(cmd)
        self.save_classes()


if __name__ == "__main__":
    from userinterface import ConsoleInterface
    ui = ConsoleInterface()
    ba = Bot_assistant(ui)
    ba.main()
