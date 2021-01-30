import bcrypt

from helpers.pwd.exceptions import GeneratePwdHashException,CheckPwdHashException

def generate_hash(pwd: str) -> bytes:
    try:
        return bcrypt.hashpw(
            password=pwd.encode(),
            salt=bcrypt.gensalt(),
        )
    except (TypeError, ValueError) as e:
        raise GeneratePwdHashException(str(e))


def check_hash(pwd: str, hash: bytes) -> None:
    try:
        res = bcrypt.checkpw(
            password=pwd.encode(),
            hashed_password=hash,
        )
    except (TypeError, ValueError) as e:
        raise CheckPwdHashException(str(e))

    if not res:
        raise CheckPwdHashException()
