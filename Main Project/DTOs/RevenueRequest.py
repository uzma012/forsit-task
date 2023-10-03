from pydantic import BaseModel
from typing import List, Optional

class RevenueRequest(BaseModel):
    start_date: str
    end_date: str
    category_id: Optional[int] = None
    
    