from sanic.exceptions import SanicException

class SanicReqValidationException(SanicException):
    status_code = 400

class SanicEmpConflictException(SanicException):
    status_code = 409

class SanicUserNotFoundException(SanicException):
    status_code = 404

class SanicRespValidationException(SanicException):
    status_code = 500

class SanicPwdHashException(SanicException):
    status_code = 500

class SanicDBException(SanicException):
    status_code = 500

class SanicEmpNotFoundException(SanicException):
    status_code = 404

class SanicMsgNotFoundException(SanicException):
    status_code = 404

class SanicAuthException(SanicException):
    status_code = 401
