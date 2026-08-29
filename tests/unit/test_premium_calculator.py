import pytest

from app.domain.entities import Address, Car
from app.domain.services import PremiumCalculatorService
from app.domain.value_objects import Money, Percentage
from app.infrastructure.config import AppSettings


def build_settings() -> AppSettings:
    return AppSettings(
        coverage_percentage=1.0,
        current_year=2022,
        gis_enabled=True,
        gis_high_risk_adjustment=0.02,
        gis_high_risk_states=["RJ"],
        gis_low_risk_adjustment=-0.02,
        gis_low_risk_states=["SC"],
        rate_increment_per_value_step=0.005,
        rate_increment_per_year=0.005,
        value_step_amount=10000.0,
    )


def test_should_apply_story_example_rate() -> None:
    service = PremiumCalculatorService(settings=build_settings())
    quote = service.calculate_quote(
        broker_fee=Money(50.0),
        car=Car(make="Toyota", model="Corolla", value=Money(100000.0), year=2012),
        deductible_percentage=Percentage(0.1),
    )
    assert quote.applied_rate.value == pytest.approx(0.10)


def test_should_calculate_premium_and_policy_limit() -> None:
    service = PremiumCalculatorService(settings=build_settings())
    quote = service.calculate_quote(
        broker_fee=Money(100.0),
        car=Car(make="Honda", model="Civic", value=Money(50000.0), year=2017),
        deductible_percentage=Percentage(0.2),
    )
    assert quote.applied_rate.value == pytest.approx(0.05)
    assert quote.calculated_premium.amount == pytest.approx(2100.0)
    assert quote.deductible_value.amount == pytest.approx(10000.0)
    assert quote.policy_limit.amount == pytest.approx(40000.0)


def test_should_apply_gis_adjustment_when_state_exists() -> None:
    service = PremiumCalculatorService(settings=build_settings())
    quote = service.calculate_quote(
        broker_fee=Money(0.0),
        car=Car(make="Fiat", model="Pulse", value=Money(20000.0), year=2020),
        deductible_percentage=Percentage(0.1),
        registration_location=Address(state="RJ"),
    )
    assert quote.applied_rate.value == pytest.approx(0.04)


def test_should_register_domain_event() -> None:
    service = PremiumCalculatorService(settings=build_settings())
    quote = service.calculate_quote(
        broker_fee=Money(0.0),
        car=Car(make="VW", model="Gol", value=Money(30000.0), year=2018),
        deductible_percentage=Percentage(0.1),
    )
    assert len(quote.events) == 1
    assert quote.events[0].premium == pytest.approx(945.0)
