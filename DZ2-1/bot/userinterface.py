from abstractinterface import AbstractInterface

class ConsoleInterface(AbstractInterface):
    __instance = None

    def __new__(cls, start_value: int = 0, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def display_chunks(self, view):
        """ Отображение многострочной информации порциями """
        ls = ''
        for txt in view():
            if len(ls) == 0:
                ls = txt
            else:
                self.print(ls.rstrip())
                if self.input('. . .') == '/q':
                    ls = ''
                    break
                ls = txt
        res = None if len(ls) == 0 else ls
        return res

    def display_contacns(self, contacts, command, key='contact', params=[]):
        """ Отображение списка контактов """
        if command == 'search':
            res = contacts.fn_search(key, params)
        else:
            res = contacts.fun_show(key, params)
        return res


    def display_notes(self, notes, command, key='note', params=[]):
        """ Отображение заметок """
        if command == 'search':
            res = notes.fn_search(key, params)
        else:
            res = notes.fun_show(key, params)
        return res


    def display_setting(self, settings, command, key='', params=[]):
        """ Отображение настроек """
        res = settings.view_setting(key)
        return res

    def display_help(self, helps, command, key=None, param=[]):
        """ Отображение справочной информации """
        res = helps.fun_help(key, param)
        return res

    def print(self, *argv):
        """ Вывод информации """
        print(*argv)

    def input(self, request=None):
        """ Ввод информации с запросом """
        return input(request)

