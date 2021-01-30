from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.req.patch_emp import ReqPatchEmpDto
from api.resp import RespEmpDto
from db.database import DBSes
from db.exceptions import DBEmpNotExistException, DBIntegrityException, DBDataException
from db.queries import emp as emp_q
from transport.sanic.endpoints.base import BaseEndpoint
from transport.sanic.exceptions import SanicEmpNotFoundException, SanicDBException






class EmpEndpoint(BaseEndpoint):

    async def method_patch(self,
                          request: Request ,
                          body: dict,
                          session: DBSes,
                          eid:int,
                          token: dict,
                          *args, **kwargs) -> BaseHTTPResponse:

        if token.get('eid') != eid:
            return await self.make_response_json(status=403)

        req_model = ReqPatchEmpDto(body)

        try:
            emp = emp_q.patch_emp(session, req_model, eid)
        except DBEmpNotExistException as e:
            raise SanicEmpNotFoundException('emp not Found')

        try:
            session.commit_session()
        except (DBIntegrityException,DBDataException) as e:
            raise SanicDBException(str(e))

        resp_model = RespEmpDto(emp)

        return await self.make_response_json(status=200, body=resp_model.dump())

    async def method_delete(
            self,
            request: Request,
            body: dict,
            session: DBSes,
            eid: int,
            token: dict,
            *args,
            **kwargs
    ) -> BaseHTTPResponse:

        if token.get('eid') != eid:
            return await self.make_response_json(status=403)

        try:
            employee = emp_q.delete_emp(session, emp_id=eid)
        except DBEmpNotExistException as e:
            raise SanicEmpNotFoundException('emp not Found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(self,
                          request: Request ,
                          body: dict,
                          session: DBSes,
                          eid:int,
                          token: dict,
                          *args, **kwargs) -> BaseHTTPResponse:

        if token.get('eid') != eid:
            return await self.make_response_json(status=403)

        # req_model = ReqPatchEmpDto(body)

        try:
            emp = emp_q.get_emp(session, emp_id = eid)
            session.commit_session()
        except DBEmpNotExistException as e:
            raise SanicEmpNotFoundException('user not Found')
        except (DBIntegrityException,DBDataException) as e:
            raise SanicDBException(str(e))

        resp_model = RespEmpDto(emp)

        return await self.make_response_json(status=200, body=resp_model.dump())
