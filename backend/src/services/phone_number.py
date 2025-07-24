from typing import Union
import uuid

from src.utils.service import Service
from src.schemas.phone_number import PhoneNumberBody, PhoneNumberPublic, ValidatePhoneNumberBody, ValidatePhoneNumberPublic, IsVerifiedPhoneNumberBody, IsVerifiedPhoneNumberPublic

class PhoneNumberService(Service):
    def __init__(self):
        super().__init__()
        
    async def send(self, data: PhoneNumberBody) -> Union[PhoneNumberPublic, tuple[int, str]]:
        pass
    
    async def validate(self, data: ValidatePhoneNumberBody) -> Union[ValidatePhoneNumberPublic, tuple[int, str]]:
        pass
    
    async def is_verified(self, data: IsVerifiedPhoneNumberBody) -> Union[IsVerifiedPhoneNumberPublic, tuple[int, str]]:
        pass


phone_number_service = PhoneNumberService()
