from agent.state import AgentState
from services.safety_checker import check_safety

def safety_node(state: AgentState):
    status, alerts = check_safety(state["raw_input"])
    return {
        "safety_status": status,
        "safety_alerts": [alert.message for alert in alerts]
    }
