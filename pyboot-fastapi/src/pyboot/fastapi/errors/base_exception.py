from fastapi import HTTPException

from pyboot.core.base_exception import BaseAppException as BE


class BaseFastapiAppException(HTTPException, BE):
    def __init__(self, code: str, message: str, http_status_code=500, headers=None, **kwargs):
        HTTPException.__init__(self, status_code=http_status_code, detail=message, headers=headers)
        BE.__init__(self, code, message, **kwargs)
        # TODO: Handle Multiple Exceptions

    def __str__(self):
        return f'{self.__class__.__name__}(code="{self.code}", message="{self.message}", https_status_code="{self.status_code}")'

    def __repr__(self):
        return f'{self.__class__.__name__}(code="{self.code}", message="{self.message}", https_status_code="{self.status_code}")'
