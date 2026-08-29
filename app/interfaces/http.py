from typing import Optional

from pydantic import BaseModel, Field

class AddressInput(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    street: Optional[str] = None


class CarInput(BaseModel):
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    value: float = Field(gt=0)
    year: int = Field(ge=1886)


class QuoteInput(BaseModel):
    broker_fee: float = Field(ge=0)
    car: CarInput
    deductible_percentage: float = Field(ge=0, le=1)
    registration_location: Optional[AddressInput] = None


class CarOutput(BaseModel):
    make: str
    model: str
    value: float
    year: int


class QuoteOutput(BaseModel):
    applied_rate: float
    calculated_premium: float
    car: CarOutput
    deductible_value: float
    policy_limit: float
