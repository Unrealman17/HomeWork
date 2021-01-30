from typing import List

from api.req import ReqCreateEmpDto, ReqPatchEmpDto
from db.database import DBSes
from db.exceptions import DBEmpExistException, DBEmpNotExistException, DBMsgNotFoundException
from db.model import DBEmp, DBMsg
from transport.sanic.exceptions import SanicMsgNotFoundException

def get_msgs(session: DBSes,user_id: int)-> List[DBMsg]:
    return session.get_msg_all(user_id)

def create_msg(session: DBSes, sender_id: int, msg: str, recipient_id: int)->DBMsg:
    msg = DBMsg(
        sender_id=sender_id,
        message=msg,
        recipient_id=recipient_id,
    )

    session.add_model(msg)

    return msg


def patch_msg(session: DBSes, message: str, mid: int, user_id: int) -> DBMsg:

    db_msg = session.get_msg_by_id(mid, user_id)
    if db_msg is None:
        raise DBMsgNotFoundException()

    setattr(db_msg, 'message', message)

    return db_msg


def delete_msg(session: DBSes, user_id: int, mid: int):
    db_msg = session.get_msg_by_id(mid=mid,user_id=user_id)

    if db_msg is None:
        raise DBMsgNotFoundException()

    setattr(db_msg, 'is_delete', True)


def get_msg(session: DBSes, user_id: int, mid: int)->DBMsg:
    db_msg = session.get_msg(user_id, mid)
    if db_msg is None:
        raise DBMsgNotFoundException()
    return db_msg