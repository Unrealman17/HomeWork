from marshmallow import Schema,fields,EXCLUDE,ValidationError, pre_load,post_load
import datetime

from api.base import RespDto

class RespMsgDtoSchema(Schema):
    id = fields.Int(required = True, allow_none = False)
    created_at = fields.DateTime(required=True)
    update_at = fields.DateTime(required=True)
    message = fields.Str(required=True)
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)


    @post_load
    @pre_load
    def deserialize_datetime(self,data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = RespMsgDtoSchema.datetime_to_iso(data['created_at'])
        if 'update_at' in data:
            data['update_at'] = RespMsgDtoSchema.datetime_to_iso(data['update_at'])

        return data


    @staticmethod
    def datetime_to_iso(dt):
        if isinstance(dt,datetime.datetime):
            return dt.isoformat()
        return dt

class RespMsgDto(RespDto, RespMsgDtoSchema):
    __schema__ = RespMsgDtoSchema