from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AwardBaseSchema(BaseModel):
    title: str
    description: str
    icon: str
    date: str

    model_config = ConfigDict(from_attributes=True)

class AwardCreate(AwardBaseSchema):
    pass

class AwardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    date: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AwardRead(AwardBaseSchema):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
