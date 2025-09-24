from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.skill import SkillCategory

class SkillBaseSchema(BaseModel):
    name: str
    icon: str
    category: SkillCategory

    model_config = ConfigDict(from_attributes=True)

class SkillCreate(SkillBaseSchema):
    rank: Optional[int] = None

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[SkillCategory] = None
    rank: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class SkillReorder(BaseModel):
    id: int
    rank: int

    model_config = ConfigDict(from_attributes=True)

class SkillRead(SkillBaseSchema):
    id: int
    rank: int
    created_at: datetime
    updated_at: Optional[datetime] = None
