from enum import Enum
from pydantic import BaseModel, Field

class DecisionType(str, Enum):
    GENERATE_ELECTRICITY = "GENERATE_ELECTRICITY"
    CAPTURE_STORE_CO2 = "CAPTURE_STORE_CO2"
    CHEMICAL_FEEDSTOCK = "CHEMICAL_FEEDSTOCK"
    VENT_SAFELY = "VENT_SAFELY"
    FLARE_GAS = "FLARE_GAS"
    EMERGENCY_STOP = "EMERGENCY_STOP"

class EnergyDecision(BaseModel):
    decision: DecisionType
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    recommendations: list[str]
    warnings: list[str] = Field(default_factory=list)
