from agent.state import AgentState
from models.report import AnalysisReport, SafetyAlert

def report_node(state: AgentState):
    # Get dynamic values determined by LLM
    safety_status = state.get("safety_status", "SAFE")
    decision = state.get("decision", "FLARE_GAS")
    
    report = AnalysisReport(
        session_id=state.get("session_id", "unknown"),
        decision=decision,
        confidence=state.get("confidence", 0.5),
        energy_potential_kwh_m3=state.get("energy_potential", 0.0),
        environmental_score=state.get("environmental_score", 0.0),
        economic_value_eur=state.get("economic_value", 0.0),
        safety_status=safety_status,
        alerts=[], # LLM handles alerts in reasoning/warnings now
        reasoning=state.get("llm_reasoning", "No reasoning provided."),
        recommendations=state.get("recommendations", []),
        electricity_strategy=state.get("electricity_strategy"),
        research_context=state.get("research_context")
    )

    return {"report": report}
