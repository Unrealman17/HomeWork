from marshmallow import Schema,fields,EXCLUDE,ValidationError, pre_load,post_load
import datetime

from api.base import RespDto

class RespEmpDtoSchema(Schema):
    id = fields.Int(required = True, allow_none = False)
    login = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    update_at = fields.DateTime(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    #position = fields.Str(required=True,allow_none=True)
    #department = fields.Str(required=True,allow_none=True)


    @post_load
    @pre_load
    def deserialize_datetime(self,data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = RespEmpDtoSchema.datetime_to_iso(data['created_at'])
        if 'update_at' in data:
            data['update_at'] = RespEmpDtoSchema.datetime_to_iso(data['update_at'])

        return data


    @staticmethod
    def datetime_to_iso(dt):
        if isinstance(dt,datetime.datetime):
            return dt.isoformat()
        return dt

class RespEmpDto(RespDto, RespEmpDtoSchema):
    __schema__ = RespEmpDtoSchema