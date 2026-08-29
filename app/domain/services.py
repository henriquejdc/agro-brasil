from app.domain.entities import Address, Car, QuoteSimulation
from app.domain.value_objects import Money, Percentage
from app.infrastructure.config import AppSettings


class PremiumCalculatorService:
    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings

    def _age_rate(self, car: Car) -> float:
        car_age = max(self._settings.current_year - car.year, 0)
        return car_age * self._settings.rate_increment_per_year

    def _gis_adjustment(self, address: Address | None) -> float:
        if not self._settings.gis_enabled or address is None or not address.state:
            return 0.0

        normalized_state = address.state.strip().upper()
        if normalized_state in self._settings.gis_high_risk_states:
            return self._settings.gis_high_risk_adjustment
        if normalized_state in self._settings.gis_low_risk_states:
            return self._settings.gis_low_risk_adjustment
        return 0.0

    def _value_rate(self, car: Car) -> float:
        steps = int(car.value.amount // self._settings.value_step_amount)
        return steps * self._settings.rate_increment_per_value_step

    def calculate_quote(
        self,
        broker_fee: Money,
        car: Car,
        deductible_percentage: Percentage,
        registration_location: Address | None = None,
    ) -> QuoteSimulation:
        applied_rate_value = (
            self._age_rate(car)
            + self._value_rate(car)
            + self._gis_adjustment(registration_location)
        )
        applied_rate = Percentage(applied_rate_value)

        base_premium = car.value.amount * applied_rate.value
        deductible_discount = base_premium * deductible_percentage.value
        calculated_premium = base_premium - deductible_discount + broker_fee.amount

        base_policy_limit = car.value.amount * self._settings.coverage_percentage
        deductible_value = base_policy_limit * deductible_percentage.value
        policy_limit = base_policy_limit - deductible_value

        quote = QuoteSimulation(
            applied_rate=applied_rate,
            broker_fee=broker_fee,
            calculated_premium=Money(calculated_premium),
            car=car,
            deductible_percentage=deductible_percentage,
            deductible_value=Money(deductible_value),
            policy_limit=Money(policy_limit),
            registration_location=registration_location,
        )
        quote.register_premium_calculated_event()
        return quote
