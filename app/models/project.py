from sqlalchemy import String, Text, TIMESTAMP, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)
    alt: Mapped[str] = mapped_column(String, nullable=True)
    docs: Mapped[str] = mapped_column(String, nullable=True)
    code: Mapped[str] = mapped_column(String, nullable=True)
    tech: Mapped[list] = mapped_column(JSON, nullable=True)
    details: Mapped[dict] = mapped_column(JSON, nullable=False)

    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now()
    )
