import os
import pathlib
import json
import re
from datetime import datetime
from botsetting import Bot_setting, get_display_lines, get_language
from bot_utils import split
from collections import UserList

sep = '---------------------------------------------------------------'
top = '--Num----Tags-------------Content------------------------------'

messages = {
    'en': {
        'bad_tag': 'Invalid tag "{tag}", valid characters: # - 1st character, the rest are "a-z", "0-9", "_" and "-"',
        'long_tag': 'The tag must be no more than {limit} characters!',
        'long_text': 'The text of note must be no more than {limit} characters!',
        'not_found': 'Notes with tag {tag} not found.',
        'tag_found': '{count} notes found with tag "{tag}".',
        'inp_numb': 'Enter the desired note number: ',
        'com_cancel': "Command canceled.",
        'bad_numb': 'Invalid number, please enter a valid one: ',
        'tag_not_impl': 'Invalid "--{key}" option for "show" command.',
        'numb_note': 'Note with number {numb}',
        'tag_note': 'Notes with the tag {tag}',
        'all_note': 'All notes',
        'empty_book': 'The notebook is empty.',
        'note_found': 'Found {count} notes.',
        'mask_not_found': 'Notes containing "{mask}" were not found.',
        'clear?': 'Delete all notes (Y - yes / N - no)? ',
        'clear_all': 'All notes removed.',
        '': ""
    },
    'ru': {
        'bad_tag': 'Некорректный тег "{tag}", допустимы символы: # - 1-й символ, остальные "a-z", "0-9", "_" и "-"',
        'long_tag': 'Тег "{tag}" должен быть не более {limit} символов!',
        'long_text': 'Текст заметки должен быть не более {limit} символов!',
        'not_found': 'Заметки с тегом {tag} не найдены.',
        'tag_found': 'С тегом "{tag}" найдено {count} заметок.',
        'inp_numb': 'Введите номер нужной заметки: ',
        'com_cancel': "Команда отменена.",
        'bad_numb': 'Некорректный номер, введите правильный: ',
        'tag_not_impl': 'Недопустимый ключ "--{key}" для команды "show".',
        'numb_note': 'Заметка с номером {numb}',
        'tag_note': 'Заметки с тегом {tag}',
        'all_note': 'Все заметки',
        'empty_book': 'Книга заметок пустая.',
        'note_found': 'Найдено {count} заметок.',
        'mask_not_found': 'Заметки, содержащие "{mask}", не найдены.',
        'clear?': 'Удалить все заметки (Y - да / N - нет)? ',
        'clear_all': 'Все заметки удалены.',
        '': ""
    },
    'uk': {
        'bad_tag': 'Некоректний тег "{tag}", допустимі символи: # - 1-й символ, інші "a-z", "0-9", "_" та "-"',
        'long_tag': 'Тег "{tag}" має містити не більше {limit} символів!',
        'long_text': 'Текст примітки має містити не більше {limit} символів!',
        'not_found': 'Нотатки з тегом {tag} не знайдені.',
        'tag_found': 'З тегом "{tag}" знайдено {count} нотаток.',
        'inp_numb': 'Введіть номер потрібної нотатки: ',
        'com_cancel': "Команда скасована.",
        'bad_numb': 'Некоректний номер, введіть правильний: ',
        'tag_not_impl': 'Недопустимий ключ "--{key}" для команди "show".',
        'numb_note': 'Нотатка з номером {numb}',
        'tag_note': 'Нотатки з тегом {tag}',
        'all_note': 'Всі нотатки',
        'empty_book': 'Книга нотаток порожня.',
        'note_found': 'Знайдено {count} нотаток.',
        'mask_not_found': 'Нотатки, що містять "{mask}", не знайдені.',
        'clear?': 'Видалити всі нотатки (Y - так / N - ні)? ',
        'clear_all': 'Всі нотатки видалені.',
        '': ""
    }
}

def get_message(key: str):
    res = messages[get_language()].get(key)
    return res if res else key

# --------------------------------------------------------------------------------------------------

class Sequence:
    __instance = None

    def __new__(cls, start_value: int = 0, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__value = start_value
        return cls.__instance

    @property
    def next_value(self):
        self.__value += 1
        return self.__value

    @property
    def curr_value(self):
        return self.__value

    def reset(self, start_value: int = 0):
        self.__value = start_value


#############################################  Note  ###############################################

class Note:
    
    def __init__(self, tags: list | str = None, content: str = None):
        self.sequence = Sequence()
        self.numb = self.sequence.next_value
        self.tags = []
        self.content = None
        self.change = datetime.now()

        self.limit_tag = 15
        self.limit_text = 80
        self.def_tag = '#default'

        if tags and content:
            self.add_tags(tags)
        if content:
            if not tags:
                self.add_tags(self.def_tag)
            self.content = self._check_content(content)


    def _check_tags(self, tags):
        tmp = set(tags)
        lst = []
        for tag in tmp:
            tg = tag.strip()
            if len(tg) > self.limit_tag:
                raise ValueError(get_message('long_tag').replace("{tag}", tg).replace('{limit}', self.limit_tag))
            if re.findall(r"(^#[a-z0-9_\-]*)", tg.lower()):
                lst.append(tg.lower())
            else:
                raise ValueError(get_message('bad_tag').replace("{tag}", tg))
        return lst

    def _check_content(self, content):
        if len(content) > self.limit_text:
            raise ValueError(get_message('bad_tag').replace('{limit}', self.limit_text))
        return content
    
    def _index_tag(self, tag):
        try:
            ind = self.tags.index(tag)
        except ValueError:
            ind = -1
        return ind
    
    def exists_tag(self, tag: str):
        ind = self._index_tag(tag)
        if ind < 0:
            return False
        return True

    def exists(self, numb: int):
        return self.numb == numb

    def add_tags(self, tags: list | str):
        if tags:
            if type(tags) == list:
                self.tags.extend(self._check_tags(tags))
            else:
                tg = split(tags, ',')
                self.tags.extend(self._check_tags(tg))
        else:
            self.tags.extend(self.def_tag)
        self.change = datetime.now()

    def remove_tag(self, tags: list | str):
        if tags:
            if type(tags) == list:
                tg = tags
            else:
                tg = split(tags, ',')
            for tag in tg:
                ind = self._index_tag(tag)
                if ind >= 0:
                    self.tags.remove(tag)
            if not self.tags:
                self.add_tags(self.def_tag)
            self.change = datetime.now()

    def edit_tag(self, tag: str, new_tag: str):
        self.add_tags(new_tag)
        self.remove_tag(tag)

    def save_content(self, content):
        self.content = self._check_content(content)
        self.change = datetime.now()

    def _form_tags(self):
        tags = []
        tg = ''
        for tag in self.tags:
            if (len(tg) + len(tag) + 1) > self.limit_tag:
                tags.append(tg)
                tg = tag
            else:
                tg = tag if not tg else tg + ' ' + tag
        if tg:
            tags.append(tg)
        return tags

    def view_note(self, tag: str = None, is_short=False):
        res = ''
        if tag:
            if self.exists_tag(tag):
                if is_short:
                    res = '{:<15} | {:<80}'.format(tag.lower(), self.content)
                else:
                    res = '{:>5} | {:<15} | {:<80}'.format(self.numb, tag.lower(), self.content)
        else:
            tags = self._form_tags()
            for numb, tg in enumerate(tags, 0):
                if numb == 0:
                    res = res + '{:>5} | {:<15} | {:<80}'.format(self.numb, tg, self.content)
                else:
                    res = res + '\n' + '{:>5} | {:^15} | {:<80}'.format(' ', tg, ' ')
        return res

    def is_search(self, mask: str):
        msk = mask.lower()
        st = str(self).lower()
        return st.find(msk) >= 0
        
    def __repr__(self):
        return self.view_note()

    def __str__(self):
        return self.view_note()

    def to_json(self):
        res = {'numb': str(self.numb),
               'tags': self.tags,
               'content': self.content,
               'change': self.change.strftime('%Y-%m-%d_%H:%M:%S')
              }
        return res

    def from_json(self, record_data):
        numb = record_data.get('numb')
        if numb:
            self.numb = int(numb)
        self.tags = record_data.get('tags')
        self.content = record_data.get('content')
        change = record_data.get('change')
        if change:
            self.change = datetime.strptime(change, '%Y-%m-%d_%H:%M:%S')
        return self.numb

###########################################  NoteBook  #############################################

class NoteBook(UserList):

    def __init__(self, interface, note: Note | str = None, tags: list | str = None):
        super().__init__()
        self.interface = interface
        self.botsetting = Bot_setting(interface)
        if note:
            self.add_note(note, tags)
        self.sequence = Sequence()

    # Функція для добавлення нотатків та тегів по ним.
    def add_note(self, note: Note | str, tags: list | str = None):
        if type(note) == Note:
            self.data.append(note)
        else:
            self.data.append(Note(tags, note))

    def _search_notes_by_tag(self, tag: str | int):
        found_notes = []
        fn = note.exists if type(tag) == int else note.exists_tag
        for note in self.data:
            # if type(tag) == int:
            #     fn = note.exists(tag)
            # else:
            #     fn = note.exists_tag(tag)
            if fn(self, tag):
                found_notes.append(note)

        if len(found_notes) == 0:
            raise ValueError(get_message('not_found').replace('{tag}', tag))

        return found_notes
    

    # Функція для редагування нотатку.
    def edit_note(self, tag: str | int, new_text: str):
        found_notes = self._search_notes_by_tag(tag)

        if len(found_notes) == 1:
            edit_note = found_notes[0]
        else:
            lst = get_message('tag_found').replace("{tag}",tag).replace("{count}", str(len(found_notes))) + '\n' + sep
            for numb, note in enumerate(found_notes, 1):
                lst = lst + '\n' + '{:^2} | {:<80}'.format(numb, note.view_note(tag, is_short=True))
            self.interface.print(lst + '\n' + sep)
            txt = get_message('inp_numb')
            while True:
                txt = self.interface.input(txt)
                if txt == '/q':
                    return get_message('com_cancel')
                try:
                    ind = int(txt) - 1
                    if ind < 1 or ind > len(found_notes):
                        raise ValueError()
                    edit_note = found_notes[ind]
                    break
                except ValueError:
                    txt = get_message('bad_numb')
        
        edit_note.save_content(new_text)
        return 'Ok'

    # Функція для пошуку нотатків по тегу.
    def search_by_tag(self, tag: str):
        found_notes = self._search_notes_by_tag(tag)
        if found_notes:
            lst = get_message('tag_found').replace("{tag}",tag).replace("{count}", str(len(found_notes))) + '\n' + top
            for note in found_notes:
                lst = lst + '\n' + str(note)
            lst = lst + '\n' + sep
        # else:
        #     lst = get_message('not_found').replace("{tag}", tag)
        return lst

    # Функція для пошуку нотатків по фрагменту тексту та тегів.
    def search_by_substring(self, mask: str):
        found_notes = []
        for note in self.data:
            if note.is_search(mask):
                found_notes.append(note)

        if found_notes:
            lst = get_message('note_found').replace("{count}", str(len(found_notes))) + '\n' + top
            for note in found_notes:
                lst = lst + '\n' + str(note)
            lst = lst + '\n' + sep
        else:
            lst = get_message('mask_not_found').replace("{mask}", mask)
        return lst

    def view_notes(self, tag: str | int = None):
        if tag:
            if type(tag) == int:
                lst = get_message('numb_note').replace("{numb}", str(tag)) + '\n' + top
            else:
                lst = get_message('tag_note').replace("{tag}", tag) + '\n' + top
            found_notes = self._search_notes_by_tag(tag)
        else:
            lst = get_message('all_note') + '\n' + top
            found_notes = self.data

        for note in found_notes:
            lst = lst + '\n' + str(note)
        lst = lst + '\n' + sep
        return lst

    def view_notes_iter(self, chunk_size = get_display_lines()):
        """
        Display all notes as chunks by chunk_size entries .

        If chunk_size == None or 0, then all notes are displayed in one chunk.
        """
        _chunk_num = 0
        _chunk_size = int(chunk_size)
        head = get_message('all_note') + ':'   # Все заметки.
        res = head + '\n' + top
        _index = 1
        try:
            for rec in self.data:
                txt = rec.view_note()
                _index = _index + txt.count('\n') + 1
                res = res  + '\n' + txt
                if (_chunk_size > 0) and (_index // _chunk_size != _chunk_num):
                    yield res
                    _chunk_num += 1
                    res = ''
            if _index == 1:
                res = get_message('empty_book')
            else:
                res = res + '\n' + sep
            if len(res) > 0:
                yield res
        except Exception as e:
            self.interface.print(str(e))
        finally:
            return 

    # Функція для редагування тегу.
    def edit_tag(self, tag, new_tag):
        found_notes = self._search_notes_by_tag(tag)
        for note in found_notes:
            note.edit_tag(tag, new_tag)
        return 'Ok'

    # Функція дял видалення замітки.
    def delete_note(self, tag):
        found_notes = self._search_notes_by_tag(tag)
        del_notes = []
        if len(found_notes) == 1:
            del_notes.extend(found_notes)
        else:
            lst = get_message('tag_found').replace("{tag}",tag).replace("{count}", str(len(found_notes))) + '\n' + sep
            for numb, note in enumerate(found_notes, 1):
                lst = lst + '\n' + '{:>5} | {:<97}'.format(numb, note.view_note(tag, is_short=True))
            self.interface.print(lst + '\n' + sep)
            txt = get_message('inp_numb')
            while True:
                txt = self.interface.input(txt)
                if txt == '/q':
                    return get_message('com_cancel')
                elif txt == '/a':
                    del_notes.extend(found_notes)
                    break
                try:
                    ind = int(txt) - 1
                    if ind < 1 or ind > len(found_notes):
                        raise ValueError()
                    del_notes.append(found_notes[ind])
                    break
                except ValueError:
                    txt = get_message('bad_numb')
        
        for note in del_notes:
            self.data.remove(note)
        return 'Ok'

    # Функція для видалення всього.
    def delete_all(self):
        ans = input(get_message('clear?'))
        if ans.upper() == 'Y':
            self.data.clear()
            # self.sequence.reset()
            return get_message('clear_all')
        return get_message('com_cancel')

    # # Функція для сортування нотатків по тегам.
    # def sort_notes_by_tag(self, tag):
    #     sorted_notes = []

    #     for note in self.notes:

    #         if tag in note['tags']:
    #             sorted_notes.append(note)

    #     if sorted_notes:
    #         sorted_notes.sort(key=lambda x: x['text'])
    #         print(f"Отсортированные заметки: {sorted_notes}")

    #         for note in sorted_notes:
    #             print(note['text'])

    #     else:
    #         print("Заметки с указанным тегом не найдены.")

    def __repr__(self):
        return self.view_notes()

    def __str__(self):
        return self.view_notes()

    def __call__(self, command, key, params):
        return self.action(command, key, params)
    
# --------------------------------------------------------------------------------------------------

    def to_json(self):
        result = []
        for record in self.data:
            result.append(record.to_json())
        return result

    def save_json(self, filename):
        file_path = pathlib.Path(os.path.dirname(filename))
        if not file_path.exists():
            file_path.mkdir(parents=True)

        data = {'notes': self.to_json()}
        with open(filename, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_json(self, filename):
        file_path = pathlib.Path(filename)
        if not file_path.exists():
            return False
        with open(filename, 'r') as file:
            data = json.load(file)
            records = data["notes"]
            self.from_json(records)
        return True

    def from_json(self, records_json):
        curr = 0
        for record_data in records_json:
            record = Note()
            self.add_note(record)
            tmp = record.from_json(record_data)
            curr = tmp if curr < tmp else curr
        
        if curr > self.sequence.curr_value:
            self.sequence.reset(curr)

# --------------------------------------------------------------------------------------------------

    def fn_add(self, key, list_params):
        if key == 'note':
            text = self.botsetting.get_param(list_params, 0, 'Text Note', 1)
            tags = self.botsetting.get_param(list_params, 1, 'Tags', 0)
            self.add_note(text, tags)
        return 'Ok'

    def fn_change(self, key, list_params):
        if key == 'note':
            tag = self.botsetting.get_param(list_params, 0, 'Tag', 1)
            text = self.botsetting.get_param(list_params, 1, 'New Text Note', 0)
            self.edit_note(text, tag)
        return 'Ok'

    def fn_delete(self, key, list_params):
        tag = self.botsetting.get_param(list_params, 0, 'Tag', 1)
        if key == 'note':
            if tag.isdecimal():
                tag = int(tag)
            self.delete_note(tag)
        elif key == 'tag':
            found_notes = self._search_notes_by_tag(tag)
            for note in found_notes:
                note.remove_tag(tag)
        return 'Ok'

    def fn_search(self, key, list_params):
        tag = self.botsetting.get_param(list_params, 0, 'Tag', 1)
        if key == 'note':
            res = self.search_by_substring(tag)
        else:
            res = self.search_by_tag(tag)
        return res

    def fun_show(self, key='note', list_params=[]):
        res = get_message('tag_not_impl').replace('{key}', key)
        if key == 'note':
            if list_params:
                tag = self.botsetting.get_param(list_params, 0, 'Tag', 1)
                if tag.isdecimal():
                    tag = int(tag)
                res = self.view_notes(tag)
            else:
                res = self.interface.display_chunks(self.view_notes_iter)
        # else:
        #     tag = self.botsetting.get_param(list_params, 0, 'Tag', 1)
        #     if tag.isdecimal():
        #         tag = int(tag)
        #     res = self.view_notes(tag)
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


##########################################################################################

if __name__ == '__main__':
    from userinterface import ConsoleInterface
    home_directory = pathlib.Path.home().joinpath('bot_assistant', 'save')

    # seq1 = Sequence(5)
    # print(seq1.value)
    # seq2 = Sequence(10)
    # print(seq2.value)
    # seq1.reset(0)
    # print(seq1.value)
    # print(seq2.value)

    # nt = Note('#1, #first', 'This is first note.')
    # print(nt)
    # print(nt.to_json())

    ui = ConsoleInterface()
    nb = NoteBook(ui)
    nb.load_json(f'{home_directory}/NoteBook.json')
    # nb.add_note('This is second note.', '#second')
    # nb.add_note('This is other note.', '#1, #third, #other')
    print(nb.view_notes())
    # print(nb.to_json())
    # nb.save_json(f'{home_directory}/NoteBook.json')
    # print(nb.search_notes_by_tag('#1'))
    
    # ls = ''
    # for txt in nb.view_notes_iter(3):
    #     if len(ls) == 0:
    #         ls = txt
    #     else:
    #         print(ls.rstrip())
    #         if input('. . .') == '/q':
    #             ls = ''
    #             break
    #         ls = txt
    # if len(ls) > 0:
    #     print(ls)

    # for note in nb:
    #     print(note)
