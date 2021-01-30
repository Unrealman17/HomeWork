from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse,json

from configs.config import AppConfig
from hooks import Context,initDb
from transport.sanic.routes import get_routes


def configure_app(conf: AppConfig,context:Context):
    initDb(config=conf,context = context)
    app = Sanic(__name__)

    for h in get_routes(conf,context):
        app.add_route(
            handler=h,
            uri=h.uri,
            methods=h.methods,
            strict_slashes=True
        )
    return app

'''
    @app.route('/', methods=["POST", ])
    async def health_endpoint(request: Request) -> HTTPResponse:
        resp = {
            'hello': 'World'
        }
        resp.update(request.json)
        return json(body=resp, status=200)
'''
