import json
from agent.state import AgentState
from models.decision import DecisionType
from utils.llm_client import get_llm
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

def decision_node(state: AgentState):
    llm = get_llm()
    
    research_context = state.get("research_context", "No research context available.")
    score = state.get("environmental_score", 0.0)

    prompt = f"""
You are an advanced industrial gas safety and energy optimization AI.
You have access to recent web research about industrial gas valorization, profitability, and ecological impacts.

═══════════════════════════════════════
INPUT DATA (POLLUTANTS ONLY)
═══════════════════════════════════════
- Composition: {state["raw_input"].model_dump()}
- Flow Rate: {state["flow_rate"]} m3/h
- Environmental Score (Calculated): {score}

═══════════════════════════════════════
RESEARCH CONTEXT (TAVILY)
═══════════════════════════════════════
{research_context}

═══════════════════════════════════════
YOUR TASK
═══════════════════════════════════════
Based ONLY on the research context provided and the input pollutants:

1. Determine the Safety Status (SAFE, WARNING, or CRITICAL) based on the toxicity/LEL levels of the pollutants.
2. Determine the Action Decision. You MUST choose the MOST PROFITABLE and MOST ECOLOGICAL option between:
   - GENERATE_ELECTRICITY (Valorisation électrique, e.g., Turbine à gaz)
   - CHEMICAL_FEEDSTOCK (Conversion chimique, Stockage ou transformation)
   - CAPTURE_STORE_CO2 (If strictly CO2)
   - FLARE_GAS (If neither is viable)
   - EMERGENCY_STOP (Must be this if Safety Status is CRITICAL)

3. Provide a reasoning that explicitly balances Profitability (rentabilité) and Ecology (écologie) based on the research.
4. Provide an electricity strategy ONLY if the decision is GENERATE_ELECTRICITY.

═══════════════════════════════════════
FINAL OUTPUT
═══════════════════════════════════════
Return ONLY this JSON block. No markdown, no extra text.
{{
  "safety_status": "SAFE" | "WARNING" | "CRITICAL",
  "decision": "GENERATE_ELECTRICITY" | "CAPTURE_STORE_CO2" | "CHEMICAL_FEEDSTOCK" | "VENT_SAFELY" | "FLARE_GAS" | "EMERGENCY_STOP",
  "reasoning": "...",
  "recommendations": ["...", "..."],
  "electricity_strategy": {{
      "recommended_technology": "...",
      "why_this_technology": "...",
      "estimated_efficiency": "...",
      "estimated_power_output_kw": 1000.0,
      "pre_treatment_steps": ["..."],
      "conversion_process": ["..."],
      "safety_precautions": ["..."],
      "estimated_revenue_per_hour_usd": 50.0,
      "co2_captured_kg_per_hour": 10.0,
      "warnings": ["..."]
  }} // ONLY INCLUDE IF DECISION IS GENERATE_ELECTRICITY
}}
"""
    
    try:
        response = llm.invoke([
            SystemMessage(content="You are an industrial AI assistant that responds ONLY in valid JSON. Do not use markdown ```json blocks."),
            HumanMessage(content=prompt)
        ])
        
        content = response.content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        
        # State update
        return {
            "decision": data.get("decision", "FLARE_GAS"),
            "safety_status": data.get("safety_status", "SAFE"),
            "llm_reasoning": data.get("reasoning", "No reasoning provided"),
            "recommendations": data.get("recommendations", []),
            "electricity_strategy": data.get("electricity_strategy"),
            "confidence": 0.85, 
            "errors": []
        }
    except Exception as e:
        return {
            "decision": "FLARE_GAS",
            "safety_status": "WARNING",
            "llm_reasoning": f"[Fallback — LLM unavailable or JSON error] {str(e)}",
            "recommendations": [
                "Review gas composition manually",
                "Check LLM connectivity"
            ],
            "confidence": 0.5,
            "errors": [f"LLM Error: {str(e)}"]
        }
