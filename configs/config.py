class SanicConfig:
    host = 'localhost'
    port = 8000
    workers = 1
    debug = False


class DBConfig:
    name = r'db.sqlite'
    url = rf'sqlite:///{name}'

class AppConfig:
    sanic: SanicConfig
    db: DBConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.db = DBConfig()
