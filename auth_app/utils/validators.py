import re

user_already_exist = 'Пользователь с таким логином уже существует'
not_equal_passwords = 'Введенные пароли не совпадают'
bad_username = 'Логин должен быть длиннее 6 символов и состоять только из латинского алфавита'
bad_password = 'Пароль не может содержать пробелы'
bad_email = 'Такого E-Mail не существует'
bad_name = 'Имя может содержать только буквы'
bad_phone = 'Номер телефона должен содержать только цифры'


def validate_username(username: str) -> object | None:
    return re.fullmatch(r'\w+', username)


def validate_name(name: str) -> object | None:
    return re.fullmatch(r'[^\s^\d]+', name)


def validate_email(email: str) -> object | None:
    return re.fullmatch(r'((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])', email)


def validate_phone(phone: str) -> object | None:
    return re.fullmatch(r'\d+', phone)


def validate_password(password: str) -> object | None:
    return re.fullmatch(r'\S+', password)
