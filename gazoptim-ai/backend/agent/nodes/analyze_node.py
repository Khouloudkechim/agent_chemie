from agent.state import AgentState
from services.gas_analyzer import analyze_mixture

def analyze_node(state: AgentState):
    gas_analysis = analyze_mixture(state["raw_input"])
    return {"gas_analysis": gas_analysis}
