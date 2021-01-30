from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoints.base import BaseEndpoint
from api.req.auth_emp import ReqAuthEmpDto

from db.queries import emp as emp_q
from db.exceptions import DBEmpNotExistException
from transport.sanic.exceptions import SanicEmpNotFoundException, SanicPwdHashException

from helpers.pwd import CheckPwdHashException, check_hash

from helpers.auth.token import create_token

class AuthEmpEndpoint(BaseEndpoint):

    async def method_post(self, request: Request ,body: dict,session,*args, **kwargs) -> BaseHTTPResponse:

        req_model = ReqAuthEmpDto(body)

        try:
            db_emp = emp_q.get_emp(session,login = req_model.login)
        except DBEmpNotExistException as e:
            raise SanicEmpNotFoundException('emp not found')

        try:
            check_hash(req_model.password, db_emp.pwd)
        except CheckPwdHashException as e:
            raise SanicPwdHashException('Wrong PWD')

        payload = {
            'eid': db_emp.id
        }

        resp_body = {
            'Auth': create_token(payload)
        }
        return await self.make_response_json(
            body = resp_body,
            status=200,
        )