from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    activities: Mapped[list["ActivityModel"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class ActivityModel(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    bac: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    planned_percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    actual_percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    ac: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)

    project: Mapped[ProjectModel] = relationship(back_populates="activities")