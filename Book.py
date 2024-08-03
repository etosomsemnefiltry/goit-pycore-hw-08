import re
from collections import UserDict
from datetime import datetime as dt, timedelta as td

class Field:
    '''Обработка любого поля.
    Все приходящие значения переводим в строку и отдаем.'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    '''Обработка имени контакта'''
    pass

class Phone(Field):
    '''Обработка номера телефона'''
    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)

    @staticmethod   
    def validate(phone):
        '''Проверка номера на соответствие требованиям'''

        # Уберем из строки возможные лишние символы
        phone = Phone.normalize_phone(phone)

        # Проверяем на нужное количество символов
        if len(phone) != 10:
            raise ValueError(f"Phone must contain 10 digits, but your is {len(phone)}")
        return True
    
    @staticmethod
    def normalize_phone(phone):
        ''' Убрать из номера все кроме + и цифр, привести к общему формату '''
        pattern = r'[^0-9]'
        return re.sub(pattern, '', phone)

class Birthday(Field):
    ''' Создание объекта даты рождения из строки '''
    def __init__(self, value):
        super().__init__(value)
        try:
            self.birthday = dt.strptime(value, "%d.%m.%Y").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use DD.MM.YYYY. {e}")
            

class Record:
    '''Обработка любой записей для Книги'''
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        ''' Добавить телефон '''
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        ''' Добавить дату дня рождения '''
        self.birthday = Birthday(birthday)

    def edit_phone(self, old_phone, new_phone):
        ''' Редактировать телефон '''
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)

    def find_phone(self, search_phone):
        ''' Найти по номеру телефона '''
        for i, phone in enumerate(self.phones):
            if phone.value == search_phone:
                return self.phones[i]

    def remove_phone(self, del_phone):
        ''' Удалить номер телефона '''
        for i, phone in enumerate(self.phones):
            if phone.value == del_phone:
                del self.phones[i]

    def __str__(self):
       return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {getattr(self.birthday, 'value', 'None') if isinstance(self.birthday, object) else 'None'}"

class AddressBook(UserDict):
    '''Реализация Книги с контактами'''

    def add_record(self, record):
        ''' Создание записи '''
        if record.name in self.data:
            print('Contact already exist')
        else:
            self.data[record.name.value] = record

    def find(self, name):
        ''' Поиск записи '''
        return self.data.get(name)
     
    def delete(self, name):
        ''' Удаление записи '''
        if name in self.data:
            del self.data[name]
