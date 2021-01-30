from marshmallow import Schema,fields,EXCLUDE,ValidationError

from api.base import ReqDto


class ReqCreateEmpDtoSchema(Schema):
    login = fields.Str(required = True, allow_none = False)
    password = fields.Str(required = True, allow_none = False)
    first_name = fields.Str(required = True, allow_none = False)
    last_name = fields.Str(required = True, allow_none = False)
    position = fields.Str(missing=None)
    department = fields.Str(missing=None)



class ReqCreateEmpDto(ReqDto, ReqCreateEmpDtoSchema):
    __schema__ = ReqCreateEmpDtoSchema