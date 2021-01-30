from marshmallow import Schema,fields,EXCLUDE,ValidationError

from api.base import ReqDto


class ReqCreateMsgDtoSchema(Schema):
    message = fields.Str(required = True, allow_none = False)
    recipient = fields.Str(required = True, allow_none = False)


class ReqCreateMsgDto(ReqDto, ReqCreateMsgDtoSchema):
    __schema__ = ReqCreateMsgDtoSchema