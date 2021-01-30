from sanic.exceptions import SanicException


class ApiValidationException(SanicException):
    status_code =  400

class ApiRespValidationException(SanicException):
    status_code =  500

