from hooks import Context
from transport.sanic.endpoints.emp.auth import AuthEmpEndpoint
from transport.sanic.endpoints.emp.emp import EmpEndpoint
from transport.sanic.endpoints.emp.get_all import AllEmpEndpoint
from transport.sanic.endpoints.health import HealthEndpoint
from transport.sanic.endpoints.emp.create import CreateEmpEndpoint
from configs.config import *
from typing import Tuple
from transport.sanic.base import SanicEndpoint
from transport.sanic.endpoints.msg import MsgEndpoint


def get_routes(config: AppConfig,context:Context) -> Tuple['SanicEndpoint']:
    return (
        HealthEndpoint(config = config, uri='/',methods = ('POST', 'GET'), context = context),
        CreateEmpEndpoint(config = config, uri='/user', methods = ['POST'], context = context),
        AuthEmpEndpoint(config=config, uri='/auth', methods=['POST'], context=context),
        EmpEndpoint(config=config, uri='/user/<eid:int>', methods=['PATCH','DELETE','GET'], context=context,auth_req=True),
        #AllEmpEndpoint(config=config, uri='/emp/all', methods=['GET'], context=context, auth_req=True),
        MsgEndpoint(config=config, uri='/msg', methods=['POST','GET'], context=context, auth_req=True),
        MsgEndpoint(config=config, uri='/msg/<mid:int>', methods=['PATCH','DELETE','GET'], context=context, auth_req=True),
    )
