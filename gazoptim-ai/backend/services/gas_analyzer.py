from models.gas_input import GasComposition
from core.constants import GAS_CONSTANTS

def analyze_mixture(composition: GasComposition) -> dict:
    comp_dict = composition.model_dump()
    total_lhv = 0.0
    total_density = 0.0
    
    # Ensure proportions
    total_pct = sum(comp_dict.values())
    if total_pct == 0:
        return {"lhv_mj_m3": 0.0, "density_kg_m3": 0.0}

    for gas, pct in comp_dict.items():
        fraction = pct / total_pct
        if gas in GAS_CONSTANTS:
            total_lhv += GAS_CONSTANTS[gas]["LHV"] * fraction
            total_density += GAS_CONSTANTS[gas]["density_stp"] * fraction

    return {
        "lhv_mj_m3": round(total_lhv, 2),
        "density_kg_m3": round(total_density, 3)
    }
