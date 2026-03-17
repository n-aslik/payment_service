from pydantic import BaseModel
from typing import Optional


class User(BaseModel): 
    username: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

    
class Login(BaseModel):
    phone_number: str
    password: str
    

    
    

