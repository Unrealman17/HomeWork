from sanic.request import Request
from sanic.response import BaseHTTPResponse, json
from http import HTTPStatus
from configs.config import SanicConfig
from typing import Iterable

from helpers.auth import read_token,ReadTokenException
from hooks import Context
from transport.sanic.exceptions import SanicAuthException


class SanicEndpoint:

    def __init__(self,
                 config:SanicConfig,
                 uri: str,
                 methods: Iterable,
                 context:Context,
                 auth_req: bool = False,
                 *args,
                 **kwargs):
        self.config = config
        self.uri = uri
        self.methods = methods
        self.context = context
        self.auth_req = auth_req
        self.__name__ = self.__class__.__name__

    async def __call__(self,request: Request, *args, **kwargs) -> BaseHTTPResponse:
        if self.auth_req:
            try:
                token = {
                    'token' : self.import_body_auth(request)
                }
                #body.update(self.import_body_auth(request))
                kwargs.update(token)
            except SanicAuthException as e:
                return await self.make_response_json(status=e.status_code)
        return await self.handler(request, *args, **kwargs)

    @staticmethod
    def import_body_headers(request: Request):
        return {
            h:v
            for h,v in request.headers.items()
            if h.lower().startswith('x-')
        }


    @staticmethod
    async def make_response_json(body: dict = None,
                                 status: int = 200 ,
                                 message: str = None,
                                 errorCode:int = None)->BaseHTTPResponse:


        if body is None:
            body = {
                'message': message or HTTPStatus(status).phrase,
                'errorCode': errorCode or status
            }

        return json(body = body, status = status)

    @staticmethod
    def import_body_auth(req: Request)-> dict:
        token = req.headers.get('Auth')
        try:
            return read_token(token)
        except ReadTokenException as e:
            raise SanicAuthException(str(e))

    @staticmethod
    def import_body_json(request: Request) -> dict:
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    async def handler(self,request :Request,*args, **kwargs) -> BaseHTTPResponse:
        body = {}

        # if self.auth_req:
        #     try:
        #         body.update(self.import_body_auth(request))
        #     except SanicAuthException as e:
        #         return await self.make_response_json(status=e.status_code)

        body.update(self.import_body_json(request))
        body.update(self.import_body_headers(request))

        return  await self._method(request,body,*args, **kwargs)

    async def _method(self,request: Request,body:dict, *args, **kwargs) -> BaseHTTPResponse:
        method = request.method.lower()
        func_name = f'method_{method}' # method_get

        if hasattr(self,func_name):
            func = getattr(self, func_name)
            return await func(request, body, *args, **kwargs)
        return await self.method_not_imp(method=method)

    async def method_not_imp(self,method:str):
        return await self.make_response_json(status = 500, message=f'Method {method.upper()} not implemented')

    async def method_get(self, request: Request,body: dict,*args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_imp(method='GET')
    async def method_post(self, request: Request,body: dict,*args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_imp(method='post')
    async def method_patch(self, request: Request,body: dict,*args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_imp(method='patch')
    async def method_delete(self, request: Request,body: dict,*args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_imp(method='delete')