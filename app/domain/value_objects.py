from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")


@dataclass(frozen=True)
class Percentage:
    value: float

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 1:
            raise ValueError("Percentage value must be between 0 and 1")
