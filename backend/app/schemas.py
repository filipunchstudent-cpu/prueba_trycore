from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer


def format_money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def format_index(value: Decimal | None) -> str | None:
    if value is None:
        return None

    return str(value.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


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

    @field_serializer("bac", "pv", "ev", "ac", "cv", "sv", "eac", "vac")
    def serialize_money(self, value: Decimal | None):
        if value is None:
            return None

        return format_money(value)

    @field_serializer("cpi", "spi")
    def serialize_index(self, value: Decimal | None):
        return format_index(value)


class ActivityWithMetrics(Activity):
    metrics: MetricsResponse


class ProjectWithMetrics(Project):
    activities: list[ActivityWithMetrics]
    metrics: MetricsResponse