from agent.state import AgentState
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from core.config import settings

def research_node(state: AgentState):
    """
    Uses Tavily API to search the web for the latest industrial safety thresholds
    and electricity generation viability for the specific gases present in the input.
    """
    # Only search if API key is present
    tavily_key = settings.TAVILY_API_KEY
    if not tavily_key or tavily_key == "your_tavily_api_key_here":
        return {"research_context": "Web search skipped: TAVILY_API_KEY not configured."}
    
    # Temporarily set os.environ for TavilySearchResults if needed
    os.environ["TAVILY_API_KEY"] = tavily_key
        
    comp = state["raw_input"].model_dump()
    # Extract the main pollutants present (> 0%)
    # Typically N2 is not a pollutant in this context.
    pollutants = ["CO", "CH4", "H2S", "SO2", "CO2"]
    present_pollutants = [gas for gas, pct in comp.items() if pct > 0.1 and gas in pollutants]
    
    if not present_pollutants:
        return {"research_context": "No significant pollutants present to research."}
        
    query = f"industrial gas valorization profitability and ecological impact: electricity generation (gas turbine) vs chemical conversion for mixture containing pollutants: {', '.join(present_pollutants)}"
    
    try:
        search_tool = TavilySearchResults(max_results=3)
        results = search_tool.invoke(query)
        
        # Format results into a single context string
        context = "Tavily Web Search Results:\n"
        if isinstance(results, list):
            for i, res in enumerate(results):
                if isinstance(res, dict):
                    context += f"[{i+1}] {res.get('content', '')}\n"
                else:
                    context += f"[{i+1}] {str(res)}\n"
        else:
            context += str(results)
            
        return {"research_context": context}
    except Exception as e:
        return {"research_context": f"Web search failed: {str(e)}"}
