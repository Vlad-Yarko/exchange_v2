from pydantic import BaseModel
from fastapi import Response


def assert_json_response(response: Response, status: int, schema: BaseModel):
    assert response.status_code == status
    data = response.json()
    assert schema(**data).model_dump() == data
