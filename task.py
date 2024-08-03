from datetime import datetime as dt, timedelta as td
from Book import AddressBook, Record, Birthday
import pickle

'''
Классы для удобства перенесены в файл Book.py
'''

def input_error(func):
    ''' Функция для декоратора, проверка валидности введенных данных '''
    def inner(*args, **kwargs):

        # Обработаем исключения для разных случаев
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the contact name please."
        except KeyError:
            return "This contact is not exist :("

    return inner

def parse_input(user_input):
    ''' Парсим команды и приводим в нижний регистр чтобы не было путаницы '''
    cmd, * args =user_input. split ()
    cmd = cmd.strip().lower()
    return cmd, * args

@input_error
def add_contact(args, book: AddressBook):
    ''' Добавляем новый контакт или делаем обновление. '''
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    # Создадим нового, если такого еще нет.
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    # Или делаем обновление существующего
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact ( args, book: AddressBook ):
    ''' Замена номера телефона контакта. '''
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    # Меняем только если такой есть
    if record is not None:
        record.edit_phone(old_phone, new_phone) 
    else:
        message = "Contact not found"
    return  message

@input_error
def show_phone( args, book: AddressBook ):
    ''' Поиск контакта '''
    name, *_ = args
    record = book.find(name)
    message = 'Contact not found.'

    #  Покажем контакт, если он есть
    if record is None:
        return message
    return f"{record.name} - {'; '.join(p.value for p in record.phones)}"

@input_error
def add_birthday( args, book: AddressBook ):
    ''' Добавление дня рождения в контакт '''
    name, birthday, *_ = args

    record = book.find(name)
    message = "Contact updated."

    # Добавляем только если такой есть
    if record is not None:
        record.add_birthday(birthday) 
    else:
        message = "Contact not found."
    return  message
    
@input_error
def show_birthday( args, book: AddressBook ):
    ''' Показываем день рождения '''
    name, *_args = args
    record = book.find(name)
    message = "Contact not found."
    # Покажем дату рождения, если она записана
    if record is not None: 
        if isinstance(record.birthday, Birthday):
            message = f"{name} - {record.birthday.value}"
        else:
            message = f"{name} - date not recorded."
    return message

def birthdays( book: AddressBook ):
    ''' Вычисляем кого поздравить в следующий 7 дней и с выходных переносим праздник на будние '''
    today_day = dt.today().date()
    count = 0
    res = ''
    
    for name, user in book.items():

        if not isinstance(user.birthday, Birthday):
            continue
        birth_date = user.birthday.birthday
        
        # Переменные для понимания, прошел день рождения или нет.
        month = True if birth_date.month == today_day.month  else False
        day = True if birth_date.day >= today_day.day else False

        # Точно ли ДР в этом месяце и еще не прошел.
        if month and day:
            # Нужно дату рождения сделать в нынешнем году
            birth_date = str(birth_date.day) + '.' + str(birth_date.month) + '.' + str(today_day.year)
            birth_date = dt.strptime(birth_date, "%d.%m.%Y").date()
            # Порядковый номер дня недели
            birth_weekday = dt.weekday(birth_date)
            add_days = 0
             
            # Если день рождение в субботу или воскресенье. Дни (0-6)
            if birth_weekday >=5:
                # Сколько дней нужно добавить к дате дня рождения, чтобы получить понедельник.
                add_days = int(7 - birth_weekday)
                # Соответственно меняем дату рождения
                birth_date = birth_date + td(days=add_days)
            
            # Нужно показывать только дни рождения в грядущие 7 дней. Сравниваем с 6, т.к. учитываем сегодняшний день
            if birth_date.day - today_day.day <= 6:

                # Запишем для передачи в консоль
                if count == 1:
                    res = f"\nНа следующей неделе поздравить:\n{res}" 
                res += f"{name} - {dt.strftime(birth_date, "%d.%m.%Y")}\n"
                count += 1

    if len(res) == 0:
        res = 'На следующей неделе дней рождения нет.'

    return res

def show_all ( book: AddressBook ):
    ''' Показываем всю книгу контактов '''
    res = ''
    # Сделаем удобный для чтения список
    for name, record in book.items():
        res += f"Contact name: {name}, phones: {'; '.join(p.value for p in record.phones)}, birthday: {record.birthday}\n"
    return res

@input_error
def delete_contact( args, book: AddressBook ):
    ''' Удаление контакта '''
    name, *_args = args
    record = book.find(name)
    message = "Contact not found."
    # Удалим, если есть
    if record is not None:
            book.delete(name)
            message = f"Contact removed."
    return message

def load_data(filename="addressbook.pkl"):
    ''' Загрузим или создадим новую книгу '''
    try:
        # Откроем уже существующую книгу
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Создадим новую книгу, если ее еще нет
        return AddressBook()  

def save_data(book, filename="addressbook.pkl"):
    ''' Сохраняем книгу '''
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def main():

    # Загружаем Книгу контактов
    book = load_data()

    print ( "Велкует к требованию!" )
    # Бот всегда слушает наши команды
    while True:
        user_input = input ( "Enter a command: " )
        command , * args = parse_input(user_input)

        # Делигируем в соответствии с командой.
        match command:
            case "close" | "exit":
                print ( "Good bye!" )
                save_data(book)
                break 
            case "hello" :
                print ( "How can I help you?" )
            case "add" :
                print (add_contact( args, book ))
            case "change" :
                print (change_contact( args, book ))
            case "phone" :
                print (show_phone( args, book ))
            case "all" :
                print(show_all( book ))
            case "add-birthday":
                print(add_birthday( args, book ))
            case "show-birthday":
                print(show_birthday( args, book ))
            case "birthdays":
                print(birthdays( book ))
            case "delete":
                print(delete_contact( args, book ))
            case _:
                print ( "Invalid command." )

if __name__ == "__main__" :
    main()