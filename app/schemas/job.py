from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator

class ListItem(BaseModel):
    text: str
    children: Optional[List["ListItem"]] = None

    model_config = ConfigDict(from_attributes=True)

ListItem.model_rebuild()

class JobBaseSchema(BaseModel):
    company: str
    description: str
    dates: str
    icon: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    details: Optional[List[ListItem]] = None
    
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, arbitrary_types_allowed=True)

class JobCreate(JobBaseSchema):
    pass

class JobUpdate(BaseModel):
    company: Optional[str] = None
    description: Optional[str] = None
    dates: Optional[str] = None
    icon: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    details: Optional[List[ListItem]] = None
    
    @field_validator("details", mode="before")
    @classmethod
    def parse_details(cls, value):
        if value is None:
            return value
        return [ListItem.model_validate(item) for item in value]

    model_config = ConfigDict(from_attributes=True)

class JobRead(JobBaseSchema):
    id: int
    details: List[ListItem] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("details", mode="before")
    @classmethod
    def parse_details(cls, value):
        if value is None:
            return value
        return [ListItem.model_validate(item) for item in value]