from agent.state import AgentState
from services.energy_calculator import calculate_energy_potential, estimate_economic_value
from services.environmental_scorer import calculate_environmental_score

def evaluate_node(state: AgentState):
    lhv = state["gas_analysis"].get("lhv_mj_m3", 0.0)
    kwh = calculate_energy_potential(lhv)
    
    score = calculate_environmental_score(state["raw_input"])
    eco_value = estimate_economic_value(kwh, state["flow_rate"])
    
    return {
        "energy_potential": kwh,
        "environmental_score": score,
        "economic_value": eco_value
    }
