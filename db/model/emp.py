from db.model.base import BaseModel
from sqlalchemy import Column, VARCHAR, INT,VARBINARY, BOOLEAN


class DBEmp(BaseModel):

    __tablename__ = 'emp'


    first_name = Column(VARCHAR(20), nullable=False)
    pwd = Column(VARBINARY(), nullable=False)
    login = Column(VARCHAR(64),unique=True)
    last_name = Column(VARCHAR(64))
    position = Column(VARCHAR(64))
    department = Column(VARCHAR(64))
    is_delete = Column(BOOLEAN,nullable=False, default=False)