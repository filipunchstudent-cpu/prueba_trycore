from decimal import Decimal

from backend.app.services.evm import (
    calculate_evm,
    consolidate_metrics,
)


def test_calculates_activity_evm_metrics():
    metrics = calculate_evm(
        bac=Decimal("1000"),
        planned_percent=Decimal("50"),
        actual_percent=Decimal("40"),
        ac=Decimal("450"),
    )

    assert metrics.bac == Decimal("1000")
    assert metrics.pv == Decimal("500")
    assert metrics.ev == Decimal("400")
    assert metrics.ac == Decimal("450")
    assert metrics.cv == Decimal("-50")
    assert metrics.sv == Decimal("-100")
    assert round(metrics.cpi,4) == round(Decimal("400") / Decimal("450"),4)
    assert metrics.spi == Decimal("0.8")
    assert metrics.eac == Decimal("1000") / metrics.cpi
    assert metrics.vac == metrics.bac - metrics.eac
    assert metrics.cost_status == "over_budget"
    assert metrics.schedule_status == "behind"


def test_marks_good_cost_and_schedule_performance():
    metrics = calculate_evm(
        bac=Decimal("1000"),
        planned_percent=Decimal("50"),
        actual_percent=Decimal("60"),
        ac=Decimal("500"),
    )

    assert metrics.pv == Decimal("500")
    assert metrics.ev == Decimal("600")
    assert metrics.cpi == Decimal("1.2")
    assert metrics.spi == Decimal("1.2")
    assert metrics.cost_status == "under_budget"
    assert metrics.schedule_status == "ahead"


def test_handles_zero_actual_cost_without_dividing_by_zero():
    metrics = calculate_evm(
        bac=Decimal("1000"),
        planned_percent=Decimal("50"),
        actual_percent=Decimal("20"),
        ac=Decimal("0"),
    )

    assert metrics.pv == Decimal("500")
    assert metrics.ev == Decimal("200")
    assert metrics.cv == Decimal("200")
    assert metrics.cpi is None
    assert metrics.eac is None
    assert metrics.vac is None
    assert metrics.cost_status == "undefined"


def test_handles_zero_planned_value_without_dividing_by_zero():
    metrics = calculate_evm(
        bac=Decimal("1000"),
        planned_percent=Decimal("0"),
        actual_percent=Decimal("20"),
        ac=Decimal("100"),
    )

    assert metrics.pv == Decimal("0")
    assert metrics.ev == Decimal("200")
    assert metrics.spi is None
    assert metrics.schedule_status == "undefined"


def test_consolidates_project_metrics_from_activity_totals():
    activity_one = calculate_evm(
        bac=Decimal("1000"),
        planned_percent=Decimal("100"),
        actual_percent=Decimal("100"),
        ac=Decimal("800"),
    )

    activity_two = calculate_evm(
        bac=Decimal("4000"),
        planned_percent=Decimal("50"),
        actual_percent=Decimal("25"),
        ac=Decimal("1500"),
    )

    activity_three = calculate_evm(
        bac=Decimal("1000"),
        planned_percent=Decimal("20"),
        actual_percent=Decimal("10"),
        ac=Decimal("200"),
    )

    total = consolidate_metrics([activity_one, activity_two, activity_three])

    assert total.bac == Decimal("6000")
    assert total.pv == Decimal("3200")
    assert total.ev == Decimal("2100")
    assert total.ac == Decimal("2500")
    assert total.cv == Decimal("-400")
    assert total.sv == Decimal("-1100")
    assert total.cpi == Decimal("2100") / Decimal("2500")
    assert total.spi == Decimal("2100") / Decimal("3200")
    assert round(total.eac,4) == round(Decimal("6000") / total.cpi,4)
    assert round(total.vac,4) == round(total.bac - total.eac,4)


def test_consolidates_empty_activity_list():
    total = consolidate_metrics([])

    assert total.bac == Decimal("0")
    assert total.pv == Decimal("0")
    assert total.ev == Decimal("0")
    assert total.ac == Decimal("0")
    assert total.cv == Decimal("0")
    assert total.sv == Decimal("0")
    assert total.cpi is None
    assert total.spi is None
    assert total.eac is None
    assert total.vac is None
    assert total.cost_status == "undefined"
    assert total.schedule_status == "undefined"