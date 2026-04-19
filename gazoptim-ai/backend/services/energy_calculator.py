from core.constants import COMBUSTION_EFFICIENCY, KWH_PER_MJ

def calculate_energy_potential(lhv_mj_m3: float) -> float:
    """
    Calculate electrical energy potential in kWh/m3
    using the LHV and assumed gas turbine efficiency.
    """
    # LHV (MJ/m3) * Efficiency * (kWh/MJ)
    kwh_m3 = lhv_mj_m3 * COMBUSTION_EFFICIENCY * KWH_PER_MJ
    return round(kwh_m3, 3)

def estimate_economic_value(kwh_m3: float, flow_rate: float, eur_per_kwh: float = 0.10) -> float:
    """
    Estimate the economic value in EUR per 1000m3
    """
    value_per_m3 = kwh_m3 * eur_per_kwh
    value_per_1000m3 = value_per_m3 * 1000
    return round(value_per_1000m3, 2)
