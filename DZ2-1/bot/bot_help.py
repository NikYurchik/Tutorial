from botsetting import get_display_lines, get_language

class Bot_help:

    def __init__(self, interface):
        self.interface = interface

    help_dict = {
        'en': {
            'header': [
                "This is a bot-assistant.",
                "Bot implemented as a console application.",
                "",
                "Executes commands:"
            ],
            'hello': [
                "'hello' - responds to 'How can I help you?', goes into interactive mode and displays the invitation '>>'.",
                "    The bot goes into interactive mode at startup without any parameters at all."
            ],
            'exit': [
                "'exit' - outputs 'Good bye!' and completes its work interactively."
            ],
#------------------------------------   AddresssBook   ---------------------------------
            'add': [
                "'add [--<key>] [<Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]]'",
                "  - saves a new contact / phone / birthday / email / address / fullname in the phonebook.",
                "  <key>: {contact | name} | phone | birthday | email | address | fullname}"
            ],
            'change': [
                "'change [--<key>] <Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]'",
                "    - saves the new phone number / birthday / email / address / fullname of an existing contact in the addressbook.",
                "    <key>: phone | birthday | email | address | fullname"
            ],
            'delete': [
                "'delete [--<key>] <Name> | <Phone>' - deleting a contact by name from the phone book / phone from a contact by name.",
                "    <key>: {contact | name} | phone"
            ],
            'search': [
                "'search <mask>' - search for contacts or notes by fragment of contacts in the addressbook."
            ],
            'show': [
                "'show [--<key>] [<Name>]' - displays the phone number for the specified contact / displays all saved contacts with phone numbers and birthday.",
                "    <key>: {contact | name} | [all] | note | setting}",
                "'show --setting' - displays all of its current settings."
            ],
#------------------------------------   NoteBook   ---------------------------------
            'add_note': [
                "'add --note <note> [{<tag> | \"<tag1>,...,<tagN>\"}]' - saves a new note."
            ],
            'change_note': [
                "'change --note <tag> [\"<note>\" [{<tag> | \"<tag1>,...,<tagN>\"}]' - change an existing note."
            ],
            'delete_note': [
                "'delete --note <tag>' - deleting a note by tag."
            ],
            'search_note': [
                "'search --note <mask>' - search for notes by fragment of notes or tags."
            ],
            'show_note': [
                "'show --note [<tag>]' - all notes are displayed if no tag is specified, otherwise only notes containing the specified tag are displayed."
            ],
            'sort_note': [
                "'sort --note [<tag>]' - Sort notes with the specified tag by other tags; if the tag is not specified, then all notes are sorted."
            ],
#------------------------------------   Settings   ---------------------------------
            'setting': [
                "'setting --<key> <value>' - set the value of the settings key.",
                "    <key>: settings keys",
                "        request_details - whether to request in the command mode the missing details of the contact;",
                "        display_birthdays - whether to display, when starting the bot, a list of contacts whose birthday falls within a specified period from the current day;",
                "        number_of_days - number of days from the current day to display the list of contacts whose birthday falls within this period.",
                "        display_lines - the number of lines to display in one chunk of the contact list or notes.",
                "        language - interface language (en - English, ru - русский, uk - український)",
                "    First, the current value of the key is displayed, then confirmation of the change is requested."
            ],
            'sort': [
                "'sort --note [<tag>]' - Sort notes with the specified tag by other tags; if the tag is not specified, then all notes are sorted.",
                "'sort --folder <source> [<target>]'",
                "   Sorts all files with subfolders.",
                "   <source> - the path to the source folder where you want to sort the files;",
                "   <target> - the path to the folder where the sorted files should be placed;",
                "              if not set, the sorted files remain in the original folder."
            ],
            'help': [
                "'help' [command] - display command help.",
                "    <key>: bot commands (hello, exit, add, change, delete, search, show, setting, help)",
                "'help --note' - displays all NoteBook subsystem commands."
            ],
            'footer': [
                "\n"
                "If the bot is launched with the key and parameters, then it performs the specified operation and exits.",
                "If the request for missing contact details is set in the settings,",
                "then in the process of performing add and change operations, the bot will interactively request the missing details."
            ]
        },
########################################################################################
        'ru': {
            'header': [
                "Это бот-помощник.",
                "Бот реализован в виде консольного приложения.",
                "",
                "Выполняет команды:"
            ],
            'hello': [
                "'hello' - отвечает 'How can I help you?', переходит в интерактивный режим и отображает приглашение '>>'.",
                "    В интерактивный режим бот переходит при запуске вообще без параметров."
            ],
            'exit': [
                "'exit' - в интерактивном режиме выводит 'Good bye!' и завершает свою работу."
            ],
#------------------------------------   AddresssBook   ---------------------------------
            'add': [
                "'add [--<key>] [<Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]]'",
                "  - сохраняет новый контакт / телефон / день рождения / электронная почта / адрес / полное имя в телефонной книге.",
                "  <key>: {contact | name} | phone | birthday | email | address | fullname}"
            ],
            'change': [
                "'change [--<key>] <Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]'",
                "    - сохраняет новый номер телефона / день рождения / электронная почта / адрес / полное имя существующего контакта в телефонной книге.",
                "    <key>: phone | birthday | email | address | fullname"
            ],
            'delete': [
                "'delete [--<key>] <Name> | <Phone>' - удаление контакта по имени из телефонной книги или телефона из контакта по имени.",
                "    <key>: {contact | name} | phone"
            ],
            'search': [
                "'search <mask>' - поиск контактов по фрагменту имени / номера телефона / дня рождения / электронной почты / адреса / полнго имени."
            ],
            'show': [
                "'show [--<key>] [<Name>]' - отображает номер телефона, день рождения, электронную почту, адрес, полное имя для указанного контакта",
                "    или отображает все сохраненные контакты со всеми заполненными реквизитами.",
                "    <key>: {contact | name} | [all] | note | setting}",
                "'show --setting' - отображает все текущие настройки."
            ],
#------------------------------------   NoteBook   ---------------------------------
            'add_note': [
                "'add --note <note> [{<tag> | \"<tag1>,...,<tagN>\"}]' - сохраняет новую заметку."
            ],
            'change_note': [
                "'change --note <tag> [\"<note>\" [{<tag> | \"<tag1>,...,<tagN>\"}]' - изменяет существующую заметку."
            ],
            'delete_note': [
                "'delete --note <tag>' - удаляет заметку по тегу."
            ],
            'search_note': [
                "'search --note <mask>' - сквозной поиск заметок по содержимому и тегам."
            ],
            'show_note': [
                "'show --note [<tag>]' - отображает все заметки, если тег не задан, иначе только заметки с заданным тегом."
            ],
            'sort_note': [
                "'sort --note [<tag>]' - Сортировать заметки с указанным тегом по остальным тегам; если тег не указан, то сортируются все заметки."
            ],
#------------------------------------   Settings   ---------------------------------
            'setting': [
                "'setting --<key> <value>' - установить значение ключа настроек.",
                "    <key>: ключи настроек",
                "        request_details - запрашивать ли в командном режиме недостающие реквизиты контакта;",
                "        display_birthdays - выводить ли при запуске бота список контактов, у которых день рождения попадает в заданный период от текущего дня;",
                "        number_of_days - количество дней от текущего дня для вывода списка контактов, у которых день рождения приходится на этот период.",
                "        display_lines - Количество отображаемых строк в одной порции вывода списка контактов или заметок.",
                "        language - interface language (en - English, ru - русский, uk - український)",
                "    Сначала выводится текущее значения ключа, затем запрашивается подтверждение изменения."
            ],
            'sort': [
                "'sort --note [<tag>]' - Сортировать заметки с указанным тегом по остальным тегам; если тег не указан, то сортируются все заметки.",
                "'sort --folder <source> [<target>]' - Сортировать все файлы с вложенными папками.",
                "   <source> - путь к исходной папке, в которой нужно отсортировать файлы;",
                "   <target> - путь к папке, в которую нужно поместить отсортированные файлы;",
                "              если не задан, то отсортированные файлы остаются в исходной папке."
            ],
            'help': [
                "'help' [command] - отобразить помощь по командам.",
                "    <key>: команды бота (hello, exit, add, change, delete, search, show, setting, help)",
                "'help --note' - отображает все команды подсистемы NoteBook."
            ],
            'footer': [
                "Если бот запускается с ключём и параметрами, то он выполняет заданную операцию и завершает работу.",
                "Если в настройках задан запрос недостающих реквизит контакта,",
                "то в процессе выполнения операций add и change бот в интерактивном режиме запросит недостающие реквизиты."
            ]
        },
        'uk': {
            'header': [
                "Це бот-помічник.",
                "Бот реалізований у вигляді консольного додатка.",
                "",
                "Виконує команди:"
            ],
            'hello': [
                "'hello' - відповідає 'How can I help you?', переходить в інтерактивний режим і відображає запрошення '>>'.",
                "    В інтерактивний режим бот переходить при запуску взагалі без параметрів."
            ],
            'exit': [
                "'exit' - в інтерактивному режимі виводить 'Good bye!' та завершує свою роботу."
            ],
#------------------------------------   AddresssBook   ---------------------------------
            'add': [
                "'add [--<key>] [<Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]]'",
                "  - зберігає новий контакт / телефон / день народження / електронна пошта / адреса / повне ім'я в телефонній книзі..",
                "  <key>: {contact | name} | phone | birthday | email | address | fullname}"
            ],
            'change': [
                "'change [--<key>] <Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]'",
                "    - зберігає новий номер телефону/день народження/електронна пошта/адреса/повне ім'я існуючого контакту в телефонній книзі..",
                "    <key>: phone | birthday | email | address | fullname"
            ],
            'delete': [
                "'delete [--<key>] <Name> | <Phone>' - видалення контакту на ім'я з телефонної книги або телефону з контакту на ім'я.",
                "    <key>: {contact | name} | phone"
            ],
            'search': [
                "'search <mask>' - пошук контактів по фрагменту імені / номера телефону / дня народження / електронної пошти / адреси / повного імені."
            ],
            'show': [
                "'show [--<key>] [<Name>]' - відображає номер телефону, день народження, електронну пошту, адресу, повне ім'я для вказаного контакту",
                "    або відображає всі збережені контакти з усіма заповненими реквізитами.",
                "    <key>: {contact | name} | [all] | note | setting}",
                "'show --setting' - відображає всі поточні налаштування."
            ],
#------------------------------------   NoteBook   ---------------------------------
            'add_note': [
                "'add --note <note> [{<tag> | \"<tag1>,...,<tagN>\"}]' - зберігає нову нотатку."
            ],
            'change_note': [
                "'change --note <tag> [\"<note>\" [{<tag> | \"<tag1>,...,<tagN>\"}]' - змінює існуючу нотатку."
            ],
            'delete_note': [
                "'delete --note <tag>' - видаляє нотатку за тегом."
            ],
            'search_note': [
                "'search --note <mask>' - наскрізний пошук нотаток за вмістом та тегами."
            ],
            'show_note': [
                "'show --note [<tag>]' - відображає всі нотатки, якщо тег не заданий, інакше тільки нотатки із заданим тегом."
            ],
            'sort_note': [
                "'sort --note [<tag>]' - відсортувати нотатки за вказаним тегом по іншим тегам; якщо тег не вказано, то сортуються всі нотатки."
            ],
#------------------------------------   Settings   ---------------------------------
            'setting': [
                "'setting --<key> <value>' - встановити значення ключа налаштувань.",
                "    <key>: ключі налаштувань",
                "        request_details - Чи вимагати в командному режимі реквізити контакту, якого не вистачає;",
                "        display_birthdays - Чи виводити при запуску бота список контактів, у яких день народження потрапляє у заданий період від поточного дня;",
                "        number_of_days - Кількість днів від поточного дня для виведення списку контактів, у яких день народження припадає на цей період.",
                "        display_lines - Кількість рядків, що відображаються в одній порції виведення списку контактів або нотаток",
                "        language - Мова інтерфейсу (en - English, ru - русский, uk - український)",
                "    Спочатку виводиться поточне значення ключа, потім запитує підтвердження зміни."
            ],
            'sort': [
                "'sort --note [<tag>]' - відсортувати нотатки за вказаним тегом по іншим тегам; якщо тег не вказано, то сортуються всі нотатки.",
                "'sort --folder <source> [<target>]' - відсортувати всі файли з вкладеними папками.",
                "   <source> - шлях до вхідної папки, в якій потрібно відсортувати файли;",
                "   <target> - шлях до папки, в яку потрібно помістити відсортовані файли;",
                "              якщо не заданий, то відсортовані файли залишаються у вхідній папці."
            ],
            'help': [
                "'help' [command] - відобразити допомогу по командам.",
                "   command: команди боту (hello, exit, add, change, delete, search, show, setting, help)",
                "'help --note' - відображує всі команди підсистеми нотаток (NoteBook)."
            ],
            'footer': [
                "Якщо бот запускається з ключем і параметрами, він виконує задану операцію і завершує роботу.",
                "Якщо в налаштуваннях заданий запит відсутніх реквізит контакту,",
                "то в процесі виконання операцій add і change бот в інтерактивному режимі запросить реквізити, що відсутні."
            ]
        }
    }

    error_text = {
        'en': "Unknown bot command.",
        'ru': "Неизвестная команда бота.",
        'uk': "Невідома команда боту."
    }

    def view_help(self, command='', key=''):
        language = get_language()
        if language not in self.help_dict:
            language = 'ru'
        lang = self.help_dict.get(language)
        res = ''
        if len(command) == 0 and len(key) == 0:
            for key, help in lang.items():
                res = res + '\n'.join(help) + '\n'
        elif key == 'note':
            for key, help in lang.items():
                if key.endswith('_note'):
                    res = res + '\n'.join(help) + '\n'
        else:
            if command not in lang:
                res = self.error_text.get(language)
                command = 'help'

            help = lang.get(command)
            res = res + '\n' + '\n'.join(help) + '\n'
        return res

    def view_help_iter(self, chunk_size = get_display_lines()):
        """
        Display the entire address book in chunks of chunk_size entries.

        If chunk_size == None or 0, then all records are displayed in one chunk.
        """
        language = get_language()
        # print(language, get_language(), chunk_size, get_display_lines())
        _index = 0
        _chunk_num = 0
        _chunk_size = int(chunk_size)
        if language not in self.help_dict:
            language = 'ru'
        lang = self.help_dict.get(language)
        res = ''
        try:
            for key, help in lang.items():
                rec = '\n'.join(help) + '\n'
                if len(res) > 0:
                    res = res + '\n' + rec
                else:
                    res = rec
                _index += len(help)
                if (_chunk_size > 0) and (_index // _chunk_size != _chunk_num):
                    yield res
                    _chunk_num += 1
                    res = ''
            if len(res) > 0:
                yield res
        finally:
            return 

    def fun_help(self, key='', list_params=[]):
        if len(list_params) > 0:
            res = self.view_help(list_params[0], key)
        else:
            res = self.interface.display_chunks(self.view_help_iter)
        return res

##########################################################################################

if __name__ == '__main__':
    from userinterface import ConsoleInterface
    ui = ConsoleInterface()
    bh = Bot_help(ui)
    # print (bh.view_help())
    # print (bh.view_help('help',language='en'))
    # print (bh.view_help('aaa'))
    # print (bh.view_help(key='note'))
    print(ui.display_chunks(bh.view_help_iter))