class ValidateException(BaseException):
    def __init__(self, errors_list: list, params: dict):
        self.errors_list = errors_list
        self.params = params
