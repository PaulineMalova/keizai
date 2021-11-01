from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class BaseSchema(BaseModel):
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    created_by: str
    updated_by: str
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
