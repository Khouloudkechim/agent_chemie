from models.decision import DecisionType
from models.gas_input import GasComposition

def get_decision(composition: GasComposition, status: str) -> DecisionType:
    """
    Python deterministic engine to make the action decision based on strict rules.
    """
    if status == "CRITICAL":
        return DecisionType.EMERGENCY_STOP

    comp = composition.model_dump()
    ch4 = comp.get("CH4", 0.0)
    co = comp.get("CO", 0.0)
    so2 = comp.get("SO2", 0.0)
    h2s = comp.get("H2S", 0.0)
    co2 = comp.get("CO2", 0.0)
    h2 = comp.get("H2", 0.0)
    n2 = comp.get("N2", 0.0)
    c3h8 = comp.get("C3H8", 0.0)

    # RULE 1: GENERATE_ELECTRICITY
    if ch4 > 20.0 or (co > 15.0 and so2 < 2.0 and h2s < 0.5):
        return DecisionType.GENERATE_ELECTRICITY

    # RULE 2: CAPTURE_STORE_CO2
    if co2 > 40.0 and ch4 < 10.0:
        return DecisionType.CAPTURE_STORE_CO2

    # RULE 3: CHEMICAL_FEEDSTOCK
    if co > 30.0 and h2 > 10.0:
        return DecisionType.CHEMICAL_FEEDSTOCK

    # RULE 4: VENT_SAFELY
    other_gases = [co, ch4, h2, so2, co2, h2s, c3h8]
    if all(g < 1.0 for g in other_gases):
        return DecisionType.VENT_SAFELY

    # Default
    return DecisionType.FLARE_GAS
