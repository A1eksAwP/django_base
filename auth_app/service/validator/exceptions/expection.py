class ValidateException(BaseException):
    def __init__(self, errors_list: list):
        self.errors_list = errors_list
