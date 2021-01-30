from db.model.base import BaseModel
from sqlalchemy import Column, VARCHAR, INT,VARBINARY, BOOLEAN


class DBMsg(BaseModel):

    __tablename__ = 'msg'


    message = Column(VARCHAR(1024), nullable=False)
    sender_id = Column(INT, nullable=False)
    recipient_id = Column(INT, nullable=False)
    is_delete = Column(BOOLEAN, nullable=False, default=False)