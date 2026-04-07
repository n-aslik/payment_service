from pydantic import BaseModel,Field
from typing import Optional
import uuid


class User(BaseModel): 
    balance: Optional[float] = 0.0

class UserBalance(BaseModel):
    balance: float
    
class Transactions(BaseModel):
    id:str
    user_id: str
    amount: float
    commission: float
    status: Optional[str] = None
    idempotency_key: Optional[str] = None
    

    
    

