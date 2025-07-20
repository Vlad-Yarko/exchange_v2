import bcrypt


class Password:
    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_binary = password.encode()
        password_hash = bcrypt.hashpw(password_binary, salt)
        return password_hash

    @staticmethod
    def check_password(input_password: str, valid_password: bytes) -> bool:
        return bcrypt.checkpw(input_password.encode(), valid_password)


pw_worker = Password()
