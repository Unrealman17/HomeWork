from hooks import Context
from transport.sanic.configure_sanic import configure_app
from configs.config import *


if __name__ == '__main__':

    context = Context()
    conf = AppConfig()
    app = configure_app(conf,context)
    app.run(host=conf.sanic.host,
            port=conf.sanic.port,
            workers=conf.sanic.workers,
            debug=conf.sanic.debug,
    )
