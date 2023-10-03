from pydantic import BaseModel
from typing import List, Optional

class SalesRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    
    