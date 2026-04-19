from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.gas_input import SensorReading, GasComposition
from api.routes.analysis import analyze_gas

router = APIRouter()

class ScenarioRequest(BaseModel):
    scenario_id: str

SCENARIOS = {
    "phosphate_plant": SensorReading(
        composition=GasComposition(SO2=15.0, CO2=65.0, N2=20.0),
        flow_rate=5000.0, temperature=150.0, pressure=1.5
    ),
    "cement_kiln": SensorReading(
        composition=GasComposition(CO=25.0, CO2=40.0, N2=35.0),
        flow_rate=10000.0, temperature=200.0, pressure=1.1
    ),
    "chemical_complex": SensorReading(
        composition=GasComposition(SO2=5.0, H2S=2.0, CO2=43.0, N2=50.0), # Note H2S is very high (2% = 20000 ppm)
        flow_rate=2000.0, temperature=100.0, pressure=2.0
    )
}

@router.post("/simulate")
async def simulate_scenario(req: ScenarioRequest):
    if req.scenario_id not in SCENARIOS:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    reading = SCENARIOS[req.scenario_id]
    return await analyze_gas(reading)
