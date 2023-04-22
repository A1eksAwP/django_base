class ValidateException(BaseException):
    def __init__(self, error_list):
        self.error_list = error_list