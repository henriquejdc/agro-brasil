import json
import os
from dataclasses import dataclass
from datetime import datetime


def _as_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_float(value: str, default: float) -> float:
    if value is None:
        return default
    return float(value)


def _as_int(value: str, default: int) -> int:
    if value is None:
        return default
    return int(value)


def _as_list(value: str) -> list[str]:
    if value is None or value.strip() == "":
        return []
    return [item.strip().upper() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class AppSettings:
    coverage_percentage: float
    current_year: int
    gis_enabled: bool
    gis_high_risk_adjustment: float
    gis_high_risk_states: list[str]
    gis_low_risk_adjustment: float
    gis_low_risk_states: list[str]
    rate_increment_per_value_step: float
    rate_increment_per_year: float
    value_step_amount: float

    @classmethod
    def load(cls) -> "AppSettings":
        defaults = {
            "coverage_percentage": 1.0,
            "current_year": datetime.now().year,
            "gis_enabled": False,
            "gis_high_risk_adjustment": 0.02,
            "gis_high_risk_states": [],
            "gis_low_risk_adjustment": -0.02,
            "gis_low_risk_states": [],
            "rate_increment_per_value_step": 0.005,
            "rate_increment_per_year": 0.005,
            "value_step_amount": 10000.0,
        }

        config_file = os.getenv("APP_CONFIG_FILE")
        if config_file:
            with open(config_file, "r", encoding="utf-8") as file:
                file_values = json.load(file)
            defaults.update(file_values)

        return cls(
            coverage_percentage=_as_float(
                os.getenv("COVERAGE_PERCENTAGE"), defaults["coverage_percentage"]
            ),
            current_year=_as_int(os.getenv("CURRENT_YEAR"), defaults["current_year"]),
            gis_enabled=_as_bool(os.getenv("GIS_ENABLED"), defaults["gis_enabled"]),
            gis_high_risk_adjustment=_as_float(
                os.getenv("GIS_HIGH_RISK_ADJUSTMENT"),
                defaults["gis_high_risk_adjustment"],
            ),
            gis_high_risk_states=_as_list(os.getenv("GIS_HIGH_RISK_STATES"))
            or defaults["gis_high_risk_states"],
            gis_low_risk_adjustment=_as_float(
                os.getenv("GIS_LOW_RISK_ADJUSTMENT"),
                defaults["gis_low_risk_adjustment"],
            ),
            gis_low_risk_states=_as_list(os.getenv("GIS_LOW_RISK_STATES"))
            or defaults["gis_low_risk_states"],
            rate_increment_per_value_step=_as_float(
                os.getenv("RATE_INCREMENT_PER_VALUE_STEP"),
                defaults["rate_increment_per_value_step"],
            ),
            rate_increment_per_year=_as_float(
                os.getenv("RATE_INCREMENT_PER_YEAR"),
                defaults["rate_increment_per_year"],
            ),
            value_step_amount=_as_float(
                os.getenv("VALUE_STEP_AMOUNT"), defaults["value_step_amount"]
            ),
        )
