from marshmallow import Schema,EXCLUDE,ValidationError

from api.exceptions import ApiValidationException, ApiRespValidationException


class ReqDto:
    __schema__: Schema

    def __init__(self,data: dict):
        try:
            valid_data = self.__schema__(unknown=EXCLUDE).load(data)
        except ValidationError as error:
            raise ApiValidationException(error.messages)
        else:
            self._import(valid_data)

    def _import(self, data: dict):
        for n, f in data.items():
            self.set(n,f)

    def set(self,k,v):
        setattr(self,k,v)

class RespDto:
    __schema__: Schema

    def __init__(self,obj, many: bool = False):
        #res = {}
        #for prop in dir(obj):
        #    if not (prop.startswith('_') or prop.endswith('_')):
        #        attr = getattr(obj,prop)
        #        if not callable(attr):
        #            res[prop] = attr
        #self._data = res
        if many:
            res = [RespDto.parse_obj(o) for o in obj]
        else:
            res = RespDto.parse_obj(obj)

        try:
            self._data = self.__schema__(unknown=EXCLUDE, many=many).load(res)
        except ValidationError as err:
            raise ApiRespValidationException(err.messages)

    @staticmethod
    def parse_obj(obj: object) -> dict:
        return{
            prop: value
            for prop in dir(obj)
            if not (prop.startswith('_') or prop.endswith('_'))
               and not callable(value := getattr(obj, prop))
        }

    def dump(self):
        return self._data