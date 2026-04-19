from pydantic import BaseModel
from typing import Optional, Union
from .decision import DecisionType

class SafetyAlert(BaseModel):
    level: str # "WARNING", "CRITICAL"
    message: str

class ElectricityStrategy(BaseModel):
    recommended_technology: str
    why_this_technology: str
    estimated_efficiency: Union[str, float]
    estimated_power_output_kw: float
    pre_treatment_steps: list[str]
    conversion_process: list[str]
    safety_precautions: list[str]
    estimated_revenue_per_hour_usd: float
    co2_captured_kg_per_hour: float
    warnings: list[str]

class AnalysisReport(BaseModel):
    session_id: str
    decision: DecisionType
    confidence: float
    energy_potential_kwh_m3: float
    environmental_score: float
    economic_value_eur: float
    safety_status: str
    alerts: list[SafetyAlert]
    reasoning: str
    recommendations: list[str]
    electricity_strategy: Optional[ElectricityStrategy] = None
    research_context: Optional[str] = None
