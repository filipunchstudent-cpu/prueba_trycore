"""Cálculo puro EVM: porcentajes 0..100 y precisión sin redondeos intermedios."""
from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal, localcontext
from typing import Literal

ZERO = Decimal("0")
ONE = Decimal("1")
PERCENT_SCALE = Decimal("100")
CALCULATION_PRECISION = 40

CostStatus = Literal["under_budget", "on_budget", "over_budget", "undefined"]
ScheduleStatus = Literal["ahead", "on_schedule", "behind", "undefined"]


@dataclass(frozen=True)
class EVMMetrics:
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
    cost_status: CostStatus
    schedule_status: ScheduleStatus


def interpret_cost(cpi: Decimal | None) -> CostStatus:
    if cpi is None:
        return "undefined"

    if cpi > ONE:
        return "under_budget"

    if cpi < ONE:
        return "over_budget"

    return "on_budget"


def interpret_schedule(spi: Decimal | None) -> ScheduleStatus:
    if spi is None:
        return "undefined"

    if spi > ONE:
        return "ahead"

    if spi < ONE:
        return "behind"

    return "on_schedule"


def _metrics_from_totals(
    *,
    bac: Decimal,
    pv: Decimal,
    ev: Decimal,
    ac: Decimal,
) -> EVMMetrics:
    cpi = ev / ac if ac != ZERO else None
    spi = ev / pv if pv != ZERO else None
    eac = bac / cpi if cpi not in (None, ZERO) else None
    vac = bac - eac if eac is not None else None

    return EVMMetrics(
        bac=bac,
        pv=pv,
        ev=ev,
        ac=ac,
        cv=ev - ac,
        sv=ev - pv,
        cpi=cpi,
        spi=spi,
        eac=eac,
        vac=vac,
        cost_status=interpret_cost(cpi),
        schedule_status=interpret_schedule(spi),
    )


def calculate_evm(
    *,
    bac: Decimal,
    planned_percent: Decimal,
    actual_percent: Decimal,
    ac: Decimal,
) -> EVMMetrics:
    """Calcula una actividad con valores previamente validados por el contrato de entrada."""
    with localcontext() as context:
        context.prec = CALCULATION_PRECISION

        pv = bac * planned_percent / PERCENT_SCALE
        ev = bac * actual_percent / PERCENT_SCALE

        return _metrics_from_totals(
            bac=bac,
            pv=pv,
            ev=ev,
            ac=ac,
        )


def consolidate_metrics(activities: Iterable[EVMMetrics]) -> EVMMetrics:
    """Suma BAC/PV/EV/AC y recalcula índices; nunca promedia CPI o SPI."""
    with localcontext() as context:
        context.prec = CALCULATION_PRECISION

        activity_list = list(activities)

        return _metrics_from_totals(
            bac=sum((activity.bac for activity in activity_list), ZERO),
            pv=sum((activity.pv for activity in activity_list), ZERO),
            ev=sum((activity.ev for activity in activity_list), ZERO),
            ac=sum((activity.ac for activity in activity_list), ZERO),
        )