from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.req.create_msg import ReqCreateMsgDto
from api.req.patch_emp import ReqPatchEmpDto
from api.req.patch_msg import ReqPatchMsgDto
from api.resp import RespEmpDto
from api.resp.msg import RespMsgDto
from db.database import DBSes
from db.exceptions import DBEmpNotExistException, DBIntegrityException, DBDataException, DBMsgNotFoundException
from db.queries import msg as msg_q
from db.queries import emp as emp_q
from helpers.pwd import generate_hash, GeneratePwdHashException
from transport.sanic.endpoints.base import BaseEndpoint
from transport.sanic.exceptions import SanicEmpNotFoundException, SanicDBException, SanicPwdHashException, \
    SanicEmpConflictException, SanicUserNotFoundException, SanicMsgNotFoundException

class MsgEndpoint(BaseEndpoint):

    async def method_patch(self,
                          request: Request ,
                          body: dict,
                          session: DBSes,
                          mid:int,
                          token: dict,
                          *args, **kwargs) -> BaseHTTPResponse:

        user_id = token.get('eid')
        if not isinstance(user_id, int):
            return await self.make_response_json(status=403)

        req_model = ReqPatchMsgDto(body)

        try:
            msg = msg_q.patch_msg(session, req_model.message, mid, user_id)
        except DBMsgNotFoundException as e:
            raise SanicMsgNotFoundException('Msg not Found')

        try:
            session.commit_session()
        except (DBIntegrityException,DBDataException) as e:
            raise SanicDBException(str(e))

        resp_model = RespMsgDto(msg)

        return await self.make_response_json(status=200, body=resp_model.dump())

    async def method_delete(
            self,
            request: Request,
            body: dict,
            session: DBSes,
            mid: int,
            token: dict,
            *args,
            **kwargs
    ) -> BaseHTTPResponse:

        user_id = token.get('eid')
        if not isinstance(user_id, int):
            return await self.make_response_json(status=403)

        try:
            msg_q.delete_msg(session, user_id=user_id,mid = mid)
        except DBMsgNotFoundException as e:
            raise SanicMsgNotFoundException('Msg not Found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(self,
                          request: Request ,
                          body: dict,
                          session: DBSes,
                          token: dict,
                          *args, **kwargs) -> BaseHTTPResponse:

        user_id = token.get('eid')
        if not isinstance(user_id, int):
            return await self.make_response_json(status=403)

        mid = kwargs['mid']
        try:
            if mid is None:
                msgs = msg_q.get_msgs(session, user_id)
                resp_model = RespMsgDto(msgs,many = True)

            else:
                msg = msg_q.get_msg(session, user_id, mid)
                resp_model = RespMsgDto(msg)

        except DBMsgNotFoundException as e:
            raise SanicMsgNotFoundException('Msg not Found')

        return await self.make_response_json(status=200, body=resp_model.dump())


    async def method_post(self, request: Request ,body: dict,session: DBSes,token: dict,*args, **kwargs) -> BaseHTTPResponse:

        sender_id = token.get('eid')
        if not isinstance(sender_id,int):
            return await self.make_response_json(status=403)

        req_model = ReqCreateMsgDto(body)

        try:
            rec = emp_q.get_emp(session,login=req_model.recipient)
        except DBEmpNotExistException as e:
            raise SanicUserNotFoundException()

        msg = msg_q.create_msg(session, sender_id, req_model.message, rec.id)

        try:
            session.commit_session()
        except (DBIntegrityException,DBDataException) as e:
            raise SanicDBException(str(e))

        resp_model = RespMsgDto(msg)

        return await self.make_response_json(body=resp_model.dump(),status=201)