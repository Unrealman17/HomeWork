from marshmallow import Schema, fields

from api.base import ReqDto

class ReqAuthEmpDtoSchema(Schema):
    login = fields.Str(required=True,allow_none=False)
    password = fields.Str(required=True, allow_none=False)

class ReqAuthEmpDto(ReqDto, ReqAuthEmpDtoSchema):
    __schema__ = ReqAuthEmpDtoSchema