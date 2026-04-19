from fastapi import APIRouter, HTTPException
import uuid
import traceback
from models.gas_input import SensorReading
from models.report import AnalysisReport
from agent.graph import build_graph

router = APIRouter()

@router.post("/analyze", response_model=AnalysisReport)
async def analyze_gas(reading: SensorReading):
    session_id = str(uuid.uuid4())

    # Initialize state
    initial_state = {
        "session_id": session_id,
        "raw_input": reading.composition,
        "flow_rate": reading.flow_rate,
        "temperature": reading.temperature,
        "pressure": reading.pressure,
        "safety_alerts": [],
        "errors": []
    }

    # Run graph
    graph = build_graph()
    try:
        final_state = graph.invoke(initial_state)
        report = final_state.get("report")
        if report is None:
            raise HTTPException(status_code=500, detail="Agent did not produce a report")
        return report
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
