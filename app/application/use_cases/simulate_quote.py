from app.application.schemas import QuoteRequest, QuoteResponse
from app.domain.entities import Address, Car
from app.domain.services import PremiumCalculatorService
from app.domain.value_objects import Money, Percentage


class SimulateQuoteUseCase:
    def __init__(self, calculator: PremiumCalculatorService) -> None:
        self._calculator = calculator

    def execute(self, data: QuoteRequest) -> QuoteResponse:
        address = None
        if any(
            [
                data.registration_city,
                data.registration_country,
                data.registration_state,
                data.registration_street,
            ]
        ):
            address = Address(
                city=data.registration_city,
                country=data.registration_country,
                state=data.registration_state,
                street=data.registration_street,
            )

        quote = self._calculator.calculate_quote(
            broker_fee=Money(data.broker_fee),
            car=Car(
                make=data.make,
                model=data.model,
                value=Money(data.value),
                year=data.year,
            ),
            deductible_percentage=Percentage(data.deductible_percentage),
            registration_location=address,
        )

        return QuoteResponse(
            applied_rate=quote.applied_rate.value,
            calculated_premium=quote.calculated_premium.amount,
            deductible_value=quote.deductible_value.amount,
            make=quote.car.make,
            model=quote.car.model,
            policy_limit=quote.policy_limit.amount,
            value=quote.car.value.amount,
            year=quote.car.year,
        )
