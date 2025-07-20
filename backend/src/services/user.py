from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository
from src.utils.password import pw_worker
from backend.src.api.utils.token import token_worker


class UserService(Service):
    def __init__(
        self,
        session: AsyncSession,
        user_repo: Repository
    ):
        super().__init__()
        self.session = session
        self.user_repo = user_repo
        self.single_repo = user_repo
        self.jwt = token_worker
        self.pw = pw_worker
