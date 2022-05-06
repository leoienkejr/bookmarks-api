'''
Exception objects for application errors

'''

from typing import Any


class ApplicationError(Exception):
    '''
    Base exception class for application errors
    '''

    def __init__(self, error_code: int, error_str: str, http_status: int, message: str | None):
        self.error_code = error_code
        self.error_str = error_str
        self.http_status = http_status
        self.message = message

        self.__dict__ = self.to_dict()

    def to_dict(self) -> dict[str, Any]:
        return {
            'error_code': self.error_code,
            'error_str': self.error_str,
            'http_status': self.http_status,
            'message': self.message
        }


EmailAlreadyInUseError = ApplicationError(error_code=1, error_str='EMAIL_ALREADY_IN_USE',
                                          http_status=400, message='Email address already in use')


exceptions_by_error_code = {
    1: EmailAlreadyInUseError
}
