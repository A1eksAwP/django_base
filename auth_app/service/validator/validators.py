import re
from django.contrib.auth.models import User
from service.validator.validator import Validator
from auth_app.service.validator import ERROR_MESSAGE
from auth_app.service.validator.exceptions.expection import ValidateException
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegisterValidator(Validator):

    def __init__(self, request_data: dict):
        self.request_data = request_data
        self.username = self.request_data['username']
        self.name = self.request_data['name']
        self.email = self.request_data['email']
        self.phone = self.request_data['phone']
        self.password = self.request_data['password']
        self.password_confirm = self.request_data['password_conf']
        self.errors = []

    def validate_username(self) -> object | None:
        return re.fullmatch(r'\w+', self.username)

    def validate_name(self) -> object | None:
        return re.fullmatch(r'[^\s^\d]+', self.name)

    def is_valid_email(self) -> bool:
        try:
            validate_email(self.email)
        except ValidationError:
            return False
        return True

    def validate_phone(self) -> object | None:
        return re.fullmatch(r'\d{1,12}', self.phone)

    def validate_password(self) -> object | None:
        return re.fullmatch(r'\S+', self.password)

    def validate(self):
        super().validate()
        if User.objects.filter(username=self.username).exists():
            self.errors.append(ERROR_MESSAGE.USER_ALREADY_EXIST)
        if User.objects.filter(email=self.email).exists():
            self.errors.append(ERROR_MESSAGE.EMAIL_ALREADY_EXIST)
        if self.password != self.password_confirm:
            self.errors.append(ERROR_MESSAGE.NOT_EQUAL_PASSWORDS)
        if not self.validate_username() or len(self.username) < 6:
            self.errors.append(ERROR_MESSAGE.BAD_USERNAME)
        if not self.validate_password():
            self.errors.append(ERROR_MESSAGE.BAD_PASSWORD)
        if not self.is_valid_email():
            self.errors.append(ERROR_MESSAGE.BAD_EMAIL)
        if not self.validate_name():
            self.errors.append(ERROR_MESSAGE.BAD_NAME)
        if not self.validate_phone():
            self.errors.append(ERROR_MESSAGE.BAD_PHONE)
        if self.errors:
            self.__throw()

    def __throw(self):
        raise ValidateException(self.errors, {
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "password_confirm": self.password_confirm,
        })


class EditValidator(RegisterValidator):
    def __init__(self, request_data: dict, db_username: str):
        self.request_data = request_data
        self.username = self.request_data['username']
        self.email = self.request_data['email']
        # self.phone = self.request_data['phone']
        self.first_name = self.request_data['first_name']
        self.last_name = self.request_data['last_name']
        self.password = ''
        self.password_confirm = ''
        self.errors = []
        self.db_username = db_username
        self.db_user = User.objects.filter(username=self.db_username).first()

    def validate(self):
        if self.db_user.username != self.username and User.objects.filter(username=self.username).exists():
            self.errors.append(ERROR_MESSAGE.USER_ALREADY_EXIST)
        if self.db_user.email != self.email and User.objects.filter(email=self.email).exists():
            self.errors.append(ERROR_MESSAGE.EMAIL_ALREADY_EXIST)
        if self.db_user.username != self.username and not self.validate_username() or len(self.username) < 6:
            self.errors.append(ERROR_MESSAGE.BAD_USERNAME)
        if self.db_user.email != self.email and not self.is_valid_email():
            self.errors.append(ERROR_MESSAGE.BAD_EMAIL)
        # if self.db_user.phone != self.phone and not self.validate_phone():
        #     self.errors.append(ERROR_MESSAGE.BAD_PHONE)
        if self.errors:
            self.__throw()

    def __throw(self):
        raise ValidateException(self.errors, {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            # "phone": self.phone,
        })
