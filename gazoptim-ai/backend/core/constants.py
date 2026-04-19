"""
Physical constants for common industrial gases.
"""

GAS_CONSTANTS = {
    "CO": {
        "LHV": 12.6,                # MJ/m3
        "gwp_factor": 1.9,          # GWP
        "LEL": 12.5,                # % vol
        "UEL": 74.0,                # % vol
        "tlv_twa": 25,              # ppm
        "combustion_temp": 1950,    # °C
        "density_stp": 1.25,        # kg/m3
    },
    "CH4": {
        "LHV": 35.8,
        "gwp_factor": 27.9,
        "LEL": 5.0,
        "UEL": 15.0,
        "tlv_twa": 1000,
        "combustion_temp": 1950,
        "density_stp": 0.717,
    },
    "H2": {
        "LHV": 10.8,
        "gwp_factor": 0,
        "LEL": 4.0,
        "UEL": 75.0,
        "tlv_twa": 0,               # Non-toxic, asphyxiant
        "combustion_temp": 2045,
        "density_stp": 0.089,
    },
    "SO2": {
        "LHV": 0,
        "gwp_factor": 0,            # Indirect effects, primarily acid rain
        "LEL": 0,
        "UEL": 0,
        "tlv_twa": 2,               # Highly toxic
        "combustion_temp": 0,
        "density_stp": 2.92,
    },
    "CO2": {
        "LHV": 0,
        "gwp_factor": 1.0,
        "LEL": 0,
        "UEL": 0,
        "tlv_twa": 5000,
        "combustion_temp": 0,
        "density_stp": 1.97,
    },
    "H2S": {
        "LHV": 22.9,
        "gwp_factor": 0,
        "LEL": 4.0,
        "UEL": 44.0,
        "tlv_twa": 10,              # Very toxic
        "combustion_temp": 1900,
        "density_stp": 1.53,
    },
    "N2": {
        "LHV": 0,
        "gwp_factor": 0,
        "LEL": 0,
        "UEL": 0,
        "tlv_twa": 0,               # Asphyxiant
        "combustion_temp": 0,
        "density_stp": 1.25,
    },
    "C3H8": {
        "LHV": 93.2,
        "gwp_factor": 3.3,
        "LEL": 2.1,
        "UEL": 9.5,
        "tlv_twa": 1000,
        "combustion_temp": 1980,
        "density_stp": 2.01,
    }
}

COMBUSTION_EFFICIENCY = 0.35  # ~35% for a gas turbine
KWH_PER_MJ = 0.277778
