import bcrypt


def hash_password(pwd: str) -> str:
    pw_bytes = pwd.encode()
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(
        password=pw_bytes,
        salt=salt,
    )
    return hashed_pw.decode()


def is_password_match(pwd: str, hashed_pwd: str) -> bool:
    is_matched = bcrypt.checkpw(
        password=pwd.encode(),
        hashed_password=hashed_pwd.encode(),
    )
    return is_matched
