from dataclasses import dataclass, field
from typing import Optional

from app.domain.events import PremiumCalculated
from app.domain.value_objects import Money, Percentage


@dataclass(frozen=True)
class Address:
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    street: Optional[str] = None


@dataclass(frozen=True)
class Car:
    make: str
    model: str
    value: Money
    year: int

    def __post_init__(self) -> None:
        if self.year < 1886:
            raise ValueError("Invalid car production year")


@dataclass
class QuoteSimulation:
    applied_rate: Percentage
    calculated_premium: Money
    car: Car
    deductible_percentage: Percentage
    deductible_value: Money
    policy_limit: Money
    registration_location: Optional[Address]
    broker_fee: Money
    events: list[PremiumCalculated] = field(default_factory=list)

    def register_premium_calculated_event(self) -> None:
        self.events.append(PremiumCalculated(premium=self.calculated_premium.amount))
