from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json, BaseHTTPResponse
from transport.sanic.base import SanicEndpoint


class HealthEndpoint(SanicEndpoint):

    async def method_get(self, request :Request,body: dict,*args, **kwargs) -> BaseHTTPResponse:
        response = {'msg':'Ky-Ky :D'}
        return  await self.make_response_json(body=response)

    async def method_post(self, request :Request,body: dict,*args, **kwargs) -> BaseHTTPResponse:
        return  await self.make_response_json(body=body)


# async def health_endpoint(request: Request) -> HTTPResponse:
#     resp = {
#         'hello': 'World'
#     }
#     return json(body=resp, status=200)