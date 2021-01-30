from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, Query
from sqlalchemy import or_,and_

from db.exceptions import DBIntegrityException,DBDataException
from db.model import BaseModel, DBEmp, DBMsg
from sqlalchemy.exc import IntegrityError,DataError

class DBSes:
    _session: Session

    def __init__(self,session: Session):
        self._session = session

    def query(self,*args, **kwargs) -> Query:
        return self._session.query(*args, **kwargs)

    def closeSes(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_emp_by_login(self, login: str) -> DBEmp:
        return self.get_emp().filter(DBEmp.login == login).first()

    def commit_session(self,need_close: bool = False) -> DBEmp:
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)
        if need_close:
            self.closeSes()

    def get_emp_by_id(self, emp_id: int) -> DBEmp:
        return self.get_emp().filter(DBEmp.id == emp_id).first()

    def get_emp_all(self) -> List[DBEmp]:
        return self.get_emp().all()

    def get_emp(self) -> Query:
        return self._session.query(DBEmp).filter(DBEmp.is_delete == False)

    def _get_msg(self) -> Query:
        return self._session.query(DBMsg).filter(DBMsg.is_delete == False)

    def get_msg_all(self, user_id: int)-> List[DBMsg]:
        return self._get_msg().filter(or_(DBMsg.sender_id == user_id, DBMsg.recipient_id == user_id)).all()

    def get_msg_by_id(self, mid: int, user_id: int) -> DBMsg:
        return self._get_msg().filter(and_(DBMsg.sender_id == user_id, DBMsg.id == mid)).first()

    def get_msg(self, user_id: int, mid: int)->DBMsg:
        return self._get_msg().filter(and_(DBMsg.sender_id == user_id, DBMsg.id == mid)).first()


class DataBase:
    connecton: Engine
    sesMaker: sessionmaker
    _test_q = 'select 1 as a'
    session: Session

    def __init__(self,connection:Engine):
        self.connecton = connection
        self.sesMaker = sessionmaker(bind=self.connecton)

    def checkConnect(self):
        self.connecton.execute(self._test_q).fetchone()

    def makeSes(self) ->DBSes:
        session = self.sesMaker()
        return DBSes(session)

    #def closeSes(self):
    #    self.session.close()

