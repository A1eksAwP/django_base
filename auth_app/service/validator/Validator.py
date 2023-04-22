import re
from django.contrib.auth.models import User
from auth_app.service.validator import ERROR_MESSAGE
from auth_app.service.validator.exceptions.ValidateExceprion import ValidateException
from service.validator.validator import Validator


class RegisterValidator(Validator):

    def __init__(self, request_data):
        self.request_data = request_data

    def validate_username(self,
                          username: str,
                          ) -> object | None:
        return re.fullmatch(r'\w+', username)

    def validate_name(self, name) -> object | None:
        return re.fullmatch(r'[^\s^\d]+', name)

    def validate_email(self, email) -> object | None:
        # TODO стандартные методы
        return re.fullmatch(r'((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])', email)

    def validate_phone(self, phone) -> object | None:
        return re.fullmatch(r'\d+', phone)

    def validate_password(self, password):
        return re.fullmatch(r'\S+', password)

    def validate(self) -> True:
        super().validate()
        errors = []
        request_data = self.request_data
        username = request_data['username']
        password = request_data['password']
        password_confirm = request_data['password_conf']
        email = request_data['email']
        name = request_data['name']
        phone_number = request_data['phone']

        if User.objects.filter(username=username).exists():
            errors.append(ERROR_MESSAGE.USER_ALREADY_EXIST)
        if User.objects.filter(email=email).exists():
            errors.append(ERROR_MESSAGE.EMAIL_ALREADY_EXIST)
        if password != password_confirm:
            errors.append(ERROR_MESSAGE.NOT_EQUAL_PASSWORDS)
        if not self.validate_username(username) or len(username) < 6:
            errors.append(ERROR_MESSAGE.BAD_USERNAME)
        if not self.validate_password(password):
            errors.append(ERROR_MESSAGE.BAD_PASSWORD)
        if not self.validate_email(email):
            errors.append(ERROR_MESSAGE.BAD_EMAIL)
        if not self.validate_name(name):
            errors.append(ERROR_MESSAGE.BAD_NAME)
        if not self.validate_phone(phone_number):
            errors.append(ERROR_MESSAGE.BAD_PHONE)

        if errors:
            self.__throw(errors)
        return True

    def save_user(self) -> list[str]:
        ...
        # TODO НЕЛЬЗЯ
        # errors = []
        # new_user = User()
        # new_user.username = self.username
        # new_user.set_password(self.password)
        # new_user.email = self.email
        # new_user.name = self.name
        # new_user.phone = self.phone
        # try:
        #     new_user.save()
        # except Exception as e:
        #     errors.append(f'Создать пользователя {self.username} не удалось. Ошибка сервера: {e}')
        # return errors

    def __throw(self, errors):
        raise ValidateException(errors)
