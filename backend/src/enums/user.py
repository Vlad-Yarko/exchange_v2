import enum


class TokenEnum(int, enum.Enum):
    REFRESH_TOKEN_EXP = 30 * 24 * 60 * 60
    ACCESS_TOKEN_EXP = 60 * 15
    
    
class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
