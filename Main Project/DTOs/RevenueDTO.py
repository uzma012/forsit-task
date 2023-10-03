from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from typing import Optional

class RevenueDTO(BaseModel):
    period_start_date: str
    period_end_date: str
    revenue: int
    