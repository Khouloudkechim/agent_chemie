from models.gas_input import GasComposition
from core.constants import GAS_CONSTANTS

def calculate_environmental_score(composition: GasComposition) -> float:
    """
    Calculate environmental score based on strict rules:
    score = 100 - (CO2*1.2) - (SO2*3.5) - (H2S*5.0) - (CO*0.8) - (CH4*0.5)
    Minimum = 0
    """
    comp_dict = composition.model_dump()
    
    co2 = comp_dict.get("CO2", 0.0)
    so2 = comp_dict.get("SO2", 0.0)
    h2s = comp_dict.get("H2S", 0.0)
    co = comp_dict.get("CO", 0.0)
    ch4 = comp_dict.get("CH4", 0.0)
    
    score = 100.0 - (co2 * 1.2) - (so2 * 3.5) - (h2s * 5.0) - (co * 0.8) - (ch4 * 0.5)
    
    return max(0.0, round(score, 2))
