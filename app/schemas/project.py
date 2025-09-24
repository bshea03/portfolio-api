from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List

class Feature(BaseModel):
    title: str
    description: str

class ProjectDetails(BaseModel):
    intro: str
    features: List[Feature]
    conclusion: str

    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    title: str
    description: str
    image: str
    alt: Optional[str] = None
    docs: Optional[str] = None
    code: Optional[str] = None
    tech: Optional[List[str]] = None
    details: Optional[ProjectDetails] = None

    model_config = ConfigDict(from_attributes=True)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    alt: Optional[str] = None
    docs: Optional[str] = None
    code: Optional[str] = None
    tech: Optional[List[str]] = None
    details: Optional[ProjectDetails] = None

    model_config = ConfigDict(from_attributes=True)

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_validator("details", mode="before")
    @classmethod
    def parse_details(cls, value):
        if value is None:
            return value
        return ProjectDetails.model_validate(value)