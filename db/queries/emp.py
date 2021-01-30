from typing import List

from api.req import ReqCreateEmpDto, ReqPatchEmpDto
from db.database import DBSes
from db.exceptions import DBEmpExistException, DBEmpNotExistException, DBMsgNotFoundException
from db.model import DBEmp, DBMsg
from transport.sanic.exceptions import SanicMsgNotFoundException


def create_emp(session: DBSes, emp: ReqCreateEmpDto, hash_pwd: bytes) -> DBEmp:
    new_emp = DBEmp(
        login = emp.login,
        pwd = hash_pwd,
        first_name = emp.first_name,
        last_name = emp.last_name,
        position=emp.position,
        department=emp.department,
    )

    if session.get_emp_by_login(new_emp.login) is not None:
        raise DBEmpExistException()

    session.add_model(new_emp)

    return new_emp


def get_emp(session: DBSes, *,login:str = None, emp_id: int = None) -> DBEmp:
    db_emp = None

    if login is not None:
        db_emp = session.get_emp_by_login(login)
    elif emp_id is not None:
        db_emp = session.get_emp_by_id(emp_id)

    if db_emp is None:
        raise DBEmpNotExistException()

    return db_emp


def patch_emp(session: DBSes, emp: ReqPatchEmpDto, eid: int) -> DBEmp:

    db_emp = session.get_emp_by_id(eid)

    for attr in emp.fields:
        if hasattr(emp,attr):
            setattr(db_emp,attr,getattr(emp,attr))

    return db_emp


def delete_emp(session: DBSes, emp_id: int)-> DBEmp:
    db_emp = session.get_emp_by_id(emp_id)
    db_emp.is_delete = True
    return db_emp


def get_emps(session: DBSes)-> List[DBEmp]:
    return session.get_emp_all()

