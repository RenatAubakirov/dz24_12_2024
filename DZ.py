from csv import DictReader, DictWriter
from os.path import exists


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    is_valid_name = False
    while not is_valid_name:
        try:
            first_name = input('Введите имя: ')
            if len(first_name) < 2:
                raise LenNumberError('Имя должно содержать как минимум 2 символа')
            last_name = "Ivanov"
            is_valid_number = False
            while not is_valid_number:
                try:
                    phone_number = int(input('Введите номер: '))
                    if len(str(phone_number)) != 11:
                        raise LenNumberError('Невалидная длина номера')
                    else:
                        is_valid_number = True
                except ValueError:
                    print('Невалидный номер!')
                    continue
                except LenNumberError as err:
                    print(err)
                    continue
            is_valid_name = True
        except LenNumberError as err:
            print(err)
            continue

    return {'Имя': first_name, 'Фамилия': last_name, 'Телефон': phone_number}


def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, data):
    with open(file_name, 'a', encoding='utf-8', newline='') as data_file:
        f_writer = DictWriter(data_file, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        if data_file.tell() == 0:
            f_writer.writeheader()
        f_writer.writerow(data)


file_name = 'phone.csv'
copy_file_name = 'phone_copy.csv'


def main():
    while True:
        command = input('Введите команду: ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print('Файл не создан, создайте его')
                continue
            print(*read_file(file_name))
        elif command == 'c':
            if not exists(file_name):
                print('Файл не создан, создайте его')
                continue

            data = read_file(file_name)
            print(*[f'{i + 1}: {line}' for i, line in enumerate(data)], sep='\n')

            try:
                line_number = int(input('Введите номер строки для копирования, из предложенных выше: '))
                if 1 <= line_number <= len(data):
                    data_to_copy = data[line_number - 1]
                    if not exists(copy_file_name):
                        create_file(copy_file_name)
                    write_file(copy_file_name, data_to_copy)
                    print(f'Строка {line_number} скопирована в файл {copy_file_name}')
                else:
                    print('Такой строки не существует, выберите другую строку.')
            except ValueError:
                print('Неверный формат номера строки. Введите целое число.')

main()