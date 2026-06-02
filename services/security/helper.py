import bcrypt


def hash_password(pwd: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd.encode("utf-8"), salt).decode("utf-8")


def verify_password(pwd: str, pwd_hash: str) -> bool:
    return bcrypt.checkpw(pwd.encode("utf=8"), pwd_hash.encode("utf-8"))


__all__ = ["verify_password", "hash_password"]
