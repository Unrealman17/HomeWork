from marshmallow import Schema, fields

from  api.base import ReqDto

class ReqPatchMsgDtoSchema(Schema):
    message = fields.Str(required=True)

class ReqPatchMsgDto(ReqDto, ReqPatchMsgDtoSchema):
    fields: list
    __schema__ = ReqPatchMsgDtoSchema

    def __init__(self,*args,**kwargs):
        self.fields=[]
        super(ReqPatchMsgDto,self).__init__(*args,**kwargs)
        
    def set(self,key,value):
        self.fields.append(key)
        super(ReqPatchMsgDto, self).set(key,value)
