from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from typing import Optional
from DTOs.RevenueDTO import RevenueDTO

class RevenueResponse(BaseModel):
    category_name: str
    revenue_by_period: List[RevenueDTO]
    

