from pydantic import BaseModel

class Schema(BaseModel):
    
    model_config = {
        "from_attributes": True,
        "extra": "forbid"
    }
