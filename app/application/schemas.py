from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QuoteRequest:
    broker_fee: float
    deductible_percentage: float
    make: str
    model: str
    registration_city: Optional[str]
    registration_country: Optional[str]
    registration_state: Optional[str]
    registration_street: Optional[str]
    value: float
    year: int


@dataclass(frozen=True)
class QuoteResponse:
    applied_rate: float
    calculated_premium: float
    deductible_value: float
    make: str
    model: str
    policy_limit: float
    value: float
    year: int
