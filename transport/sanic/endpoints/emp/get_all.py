from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.req.patch_emp import ReqPatchEmpDto
from api.resp import RespEmpDto
from db.database import DBSes
from db.exceptions import DBEmpNotExistException, DBIntegrityException, DBDataException
from db.queries import emp as emp_q
from transport.sanic.endpoints.base import BaseEndpoint
from transport.sanic.exceptions import SanicEmpNotFoundException, SanicDBException


class AllEmpEndpoint(BaseEndpoint):

    async def method_get(self,
                          request: Request ,
                          body: dict,
                          session: DBSes,
                          *args, **kwargs) -> BaseHTTPResponse:
        db_emp = emp_q.get_emps(session)
        resp_model = RespEmpDto(db_emp,many = True)

        return await self.make_response_json(status=200, body=resp_model.dump())