from fastapi import FastAPI

from app.application.use_cases.simulate_quote import SimulateQuoteUseCase
from app.domain.services import PremiumCalculatorService
from app.infrastructure.config import AppSettings
from app.routes import create_router


def create_app() -> FastAPI:
    settings = AppSettings.load()
    calculator = PremiumCalculatorService(settings=settings)
    use_case = SimulateQuoteUseCase(calculator=calculator)

    application = FastAPI(title="Car Insurance Premium Simulator")
    application.include_router(create_router(use_case=use_case))
    return application

app = create_app()
