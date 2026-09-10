from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ActivityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    bac: Decimal = Field(ge=0)
    planned_percent: Decimal = Field(ge=0, le=100)
    actual_percent: Decimal = Field(ge=0, le=100)
    ac: Decimal = Field(ge=0)


class Activity(ActivityCreate):
    id: int


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class Project(ProjectCreate):
    id: int
    activities: list[Activity] = []


class MetricsResponse(BaseModel):
    bac: Decimal
    pv: Decimal
    ev: Decimal
    ac: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    cost_status: str
    schedule_status: str

    model_config = ConfigDict(from_attributes=True)


class ActivityWithMetrics(Activity):
    metrics: MetricsResponse


class ProjectWithMetrics(Project):
    activities: list[ActivityWithMetrics]
    metrics: MetricsResponse