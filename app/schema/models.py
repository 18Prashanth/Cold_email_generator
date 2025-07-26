from pydantic import BaseModel
from typing import List

class Links(BaseModel):
    url: str


class email_response(BaseModel):
    emails: List[str]