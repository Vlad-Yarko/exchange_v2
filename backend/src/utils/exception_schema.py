from typing import Union

from pydantic import BaseModel


class ExceptionSchema(BaseModel):
    detail: Union[str, list]
