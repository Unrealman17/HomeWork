from sqlalchemy import Column, VARCHAR, VARBINARY

from db.model import BaseModel

class User(BaseModel):

    __tablename__ = 'user'

    login = Column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )

    pwd = Column(
        VARBINARY(),
        nullable=False,
    )