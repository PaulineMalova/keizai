from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class BaseInput(BaseModel):
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    created_by: Optional[str]
    updated_by: Optional[str]
    is_active: Optional[bool] = True
    deleted_by: Optional[str] = None
    deleted_at: Optional[datetime] = None
