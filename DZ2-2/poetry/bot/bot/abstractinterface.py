from abc import ABC, abstractmethod

class AbstractInterface(ABC):

    @abstractmethod
    def display_chunks(self):
        """ Отображение многострочной информации порциями """
        pass

    @abstractmethod
    def display_contacns(self):
        """ Отображение списка контактов """
        pass

    @abstractmethod
    def display_notes(self):
        """ Отображение заметок """
        pass

    @abstractmethod
    def display_setting(self):
        """ Отображение настроек """
        pass

    @abstractmethod
    def display_help(self):
        """ Отображение справочной информации """
        pass

    @abstractmethod
    def print(self):
        """ Вывод информации """
        pass

    @abstractmethod
    def input(self):
        """ Ввод информации с запросом """
        pass


