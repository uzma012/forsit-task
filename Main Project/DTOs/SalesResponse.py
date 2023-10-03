from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from typing import Optional

class SalesResponse(BaseModel):
    sale_date: str
    total_sale_amount: int
    product_id: Optional[int] = None
    category_id: Optional[int] = None