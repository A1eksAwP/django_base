import re
from django.contrib.auth.models import User
from auth_app.service.validator.ERROR_MESSAGE import USER_ALREADY_EXIST, EMAIL_ALREADY_EXIST, \
    NOT_EQUAL_PASSWORDS, BAD_USERNAME, BAD_PASSWORD, BAD_EMAIL, BAD_NAME, BAD_PHONE


class RegisterValidator:

    def __init__(self, username: str, password: str, password_confirm: str, email: str, name: str, phone_number: str):
        self.username = username
        self.name = name
        self.email = email
        self.phone = phone_number
        self.password = password
        self.password_confirm = password_confirm

    def validate_username(self) -> object | None:
        return re.fullmatch(r'\w+', self.username)

    def validate_name(self) -> object | None:
        return re.fullmatch(r'[^\s^\d]+', self.name)

    def validate_email(self) -> object | None:
        return re.fullmatch(r'((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])', self.email)

    def validate_phone(self) -> object | None:
        return re.fullmatch(r'\d+', self.phone)

    def validate_password(self) -> object | None:
        return re.fullmatch(r'\S+', self.password)

    def validate_register(self) -> list[str]:
        errors = []
        if User.objects.filter(username=self.username).exists():
            errors.append(USER_ALREADY_EXIST)
        if User.objects.filter(email=self.email).exists():
            errors.append(EMAIL_ALREADY_EXIST)
        if self.password != self.password_confirm:
            errors.append(NOT_EQUAL_PASSWORDS)
        if not self.validate_username() or len(self.username) < 6:
            errors.append(BAD_USERNAME)
        if not self.validate_password():
            errors.append(BAD_PASSWORD)
        if not self.validate_email():
            errors.append(BAD_EMAIL)
        if not self.validate_name():
            errors.append(BAD_NAME)
        if not self.validate_phone():
            errors.append(BAD_PHONE)
        return errors

    def save_user(self) -> list[str]:
        errors = []
        new_user = User()
        new_user.username = self.username
        new_user.set_password(self.password)
        new_user.email = self.email
        new_user.name = self.name
        new_user.phone = self.phone
        try:
            new_user.save()
        except Exception as e:
            errors.append(f'Создать пользователя {self.username} не удалось. Ошибка сервера: {e}')
        return errors
