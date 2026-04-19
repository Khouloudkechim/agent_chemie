from models.gas_input import GasComposition
from models.report import SafetyAlert
from core.constants import GAS_CONSTANTS

def check_safety(composition: GasComposition) -> tuple[str, list[SafetyAlert]]:
    """
    Check strict safety conditions for SO2, H2S, and CO.
    Returns (status, alerts). Status can be SAFE, WARNING, CRITICAL.
    """
    comp_dict = composition.model_dump()
    alerts = []
    status = "SAFE"

    so2 = comp_dict.get("SO2", 0.0)
    h2s = comp_dict.get("H2S", 0.0)
    co = comp_dict.get("CO", 0.0)

    # EMERGENCY STOP CONDITIONS (CRITICAL)
    if so2 > 5.0 or h2s > 1.0 or co > 50.0:
        status = "CRITICAL"
        if so2 > 5.0:
            alerts.append(SafetyAlert(level="CRITICAL", message=f"SO2 at {so2}% exceeds CRITICAL threshold of 5%."))
        if h2s > 1.0:
            alerts.append(SafetyAlert(level="CRITICAL", message=f"H2S at {h2s}% exceeds CRITICAL threshold of 1%."))
        if co > 50.0:
            alerts.append(SafetyAlert(level="CRITICAL", message=f"CO at {co}% exceeds CRITICAL threshold of 50%."))
        return status, alerts  # First match wins for CRITICAL

    # WARNING CONDITIONS
    if so2 > 2.0 or h2s > 0.5 or co > 20.0:
        status = "WARNING"
        if so2 > 2.0:
            alerts.append(SafetyAlert(level="WARNING", message=f"SO2 at {so2}% exceeds WARNING threshold of 2%."))
        if h2s > 0.5:
            alerts.append(SafetyAlert(level="WARNING", message=f"H2S at {h2s}% exceeds WARNING threshold of 0.5%."))
        if co > 20.0:
            alerts.append(SafetyAlert(level="WARNING", message=f"CO at {co}% exceeds WARNING threshold of 20%."))

    return status, alerts
