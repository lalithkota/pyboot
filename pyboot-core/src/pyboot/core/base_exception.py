class BaseAppException(Exception):
    def __init__(self, code: str, message: str, *kw):
        super().__init__(*kw)
        self.code = code
        self.message = message
