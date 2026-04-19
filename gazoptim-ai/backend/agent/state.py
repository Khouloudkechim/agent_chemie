from typing import TypedDict, Optional
from models.gas_input import GasComposition
from models.decision import DecisionType

class AgentState(TypedDict, total=False):
    session_id: str
    raw_input: GasComposition
    flow_rate: float
    temperature: float
    pressure: float
    gas_analysis: dict           # physical properties of the mixture
    safety_status: str           # SAFE / WARNING / CRITICAL
    safety_alerts: list
    research_context: str        # Tavily search results
    energy_potential: float      # kWh/m3
    environmental_score: float   # 0–100
    economic_value: float        # EUR/1000m3
    llm_reasoning: str
    decision: str                # DecisionType value
    confidence: float
    recommendations: list
    electricity_strategy: dict   # Only if GENERATE_ELECTRICITY
    report: Optional[dict]
    errors: list
