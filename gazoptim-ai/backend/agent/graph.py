from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes.analyze_node import analyze_node
from agent.nodes.research_node import research_node
from agent.nodes.evaluate_node import evaluate_node
from agent.nodes.decision_node import decision_node
from agent.nodes.report_node import report_node

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analyze_node", analyze_node)
    workflow.add_node("research_node", research_node)
    workflow.add_node("evaluate_node", evaluate_node)
    workflow.add_node("decision_node", decision_node)
    workflow.add_node("report_node", report_node)
    
    workflow.add_edge(START, "analyze_node")
    workflow.add_edge("analyze_node", "research_node")
    workflow.add_edge("research_node", "evaluate_node")
    workflow.add_edge("evaluate_node", "decision_node")
    workflow.add_edge("decision_node", "report_node")
    workflow.add_edge("report_node", END)
    
    return workflow.compile()
