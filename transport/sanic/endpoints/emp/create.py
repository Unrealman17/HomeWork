from sanic.request import Request
from sanic.response import BaseHTTPResponse

from db.database import DBSes
from transport.sanic.endpoints.base import BaseEndpoint
from api.req import ReqCreateEmpDto
from api.resp import RespEmpDto

from db.queries import emp as emp_q
from helpers.pwd import generate_hash
from helpers.pwd import CheckPwdHashException,GeneratePwdHashException

from transport.sanic.exceptions import SanicPwdHashException, SanicDBException, SanicEmpConflictException
from db.exceptions import DBIntegrityException,DBDataException,DBEmpExistException

class CreateEmpEndpoint(BaseEndpoint):

    async def method_post(self, request: Request ,body: dict,session: DBSes,*args, **kwargs) -> BaseHTTPResponse:

        req_model = ReqCreateEmpDto(body)

        try:
            hash_pwd = generate_hash(req_model.password)
        except GeneratePwdHashException as e:
            raise SanicPwdHashException(str(e))

        try:
            db_emp = emp_q.create_emp(session, req_model,hash_pwd)
        except DBEmpExistException as e:
            raise SanicEmpConflictException('Login is busy')
        try:
            session.commit_session()
        except (DBIntegrityException,DBDataException) as e:
            raise SanicDBException(str(e))



        resp_model = RespEmpDto(db_emp)

        return await self.make_response_json(body=resp_model.dump(),status=201)