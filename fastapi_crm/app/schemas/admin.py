from pydantic import BaseModel

class Admin(BaseModel):
    id: str
    pw: str
