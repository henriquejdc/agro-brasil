from fastapi import APIRouter

from app.application.schemas import QuoteRequest
from app.application.use_cases.simulate_quote import SimulateQuoteUseCase
from app.interfaces.http import CarOutput, QuoteInput, QuoteOutput


def create_router(use_case: SimulateQuoteUseCase) -> APIRouter:
    router = APIRouter()

    @router.post("/quotes/simulate", response_model=QuoteOutput)
    def simulate_quote(payload: QuoteInput) -> QuoteOutput:
        location = payload.registration_location
        response = use_case.execute(
            QuoteRequest(
                broker_fee=payload.broker_fee,
                deductible_percentage=payload.deductible_percentage,
                make=payload.car.make,
                model=payload.car.model,
                registration_city=location.city if location else None,
                registration_country=location.country if location else None,
                registration_state=location.state if location else None,
                registration_street=location.street if location else None,
                value=payload.car.value,
                year=payload.car.year,
            )
        )
        return QuoteOutput(
            applied_rate=response.applied_rate,
            calculated_premium=response.calculated_premium,
            car=CarOutput(
                make=response.make,
                model=response.model,
                value=response.value,
                year=response.year,
            ),
            deductible_value=response.deductible_value,
            policy_limit=response.policy_limit,
        )

    return router