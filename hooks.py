from configs.config import AppConfig
from sqlalchemy import create_engine
from db.database import DataBase


class ContextLockedException(Exception):
    pass

class Context:

    def __init__(self):
        self.locked = False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def set(self,k,v):
        if self.locked:
            raise ContextLockedException
        setattr(self,k,v)

def initDb(config: AppConfig, context:Context):
    uri = config.db.url #r'sqlite///db.sqlite'
    engin = create_engine(
        uri,
        pool_pre_ping=True
    )
    db = DataBase(connection=engin)
    db.checkConnect()

    context.set('db',db)
