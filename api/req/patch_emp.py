from marshmallow import Schema, fields

from  api.base import ReqDto

class ReqPatchEmpDtoSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()

class ReqPatchEmpDto(ReqDto, ReqPatchEmpDtoSchema):
    fields: list
    __schema__ = ReqPatchEmpDtoSchema

    def __init__(self,*args,**kwargs):
        self.fields=[]
        super(ReqPatchEmpDto,self).__init__(*args,**kwargs)
        
    def set(self,key,value):
        self.fields.append(key)
        super(ReqPatchEmpDto, self).set(key,value)
