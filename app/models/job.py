import json
from sqlalchemy import JSON, TIMESTAMP, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base

class Job(Base):
  __tablename__ = "jobs"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  company: Mapped[str] = mapped_column(String, nullable=False)
  icon: Mapped[str] = mapped_column(String, nullable=True)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  dates: Mapped[str] = mapped_column(String, nullable=False)
  location: Mapped[str] = mapped_column(String, nullable=True)
  skills: Mapped[list] = mapped_column(JSON, nullable=True)
  details: Mapped[list] = mapped_column(JSON, nullable=True)
  created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
  updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), server_onupdate=func.now()
)