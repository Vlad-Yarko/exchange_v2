from typing import Union
import uuid

from src.utils.service import Service
from src.schemas.email import EmailPublic, EmailBody, ValidateEmailPublic, ValidateEmailBody
from src.utils.repository import Repository


class EmailService(Service):
    def __init__(self):
        super().__init__()
        
    async def send_email(self, data: EmailBody) -> Union[EmailPublic, tuple[int, str]]:
        pass
    
    async def validate_email(self, data: ValidateEmailBody) -> Union[ValidateEmailPublic, tuple[int, str]]:
        pass
    
    async def is_verified_email(self, email: str) -> Union[bool, tuple[int, str]]:
        pass


email_service = EmailService()
