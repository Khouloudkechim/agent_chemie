from fastapi import APIRouter, HTTPException
from services.dataset_service import (
    get_all_samples, get_sample_by_id,
    row_to_sensor_reading, get_random_sample
)
from api.routes.analysis import analyze_gas

router = APIRouter()


@router.get("/dataset")
async def list_dataset():
    """List all industrial pollutant entries from the dataset."""
    samples = get_all_samples()
    return {
        "total": len(samples),
        "entries": [
            {
                "id": int(s["id"]),
                "name": s["name"],
                "industry_type": s["industry_type"],
                "composition": {
                    "SO2": float(s["SO2"]),
                    "H2S": float(s["H2S"]),
                    "CO":  float(s["CO"]),
                    "CO2": float(s["CO2"]),
                    "N2":  float(s["N2"]),
                    "CH4": float(s["CH4"]),
                },
                "flow_rate": float(s["flow_rate"]),
                "temperature": float(s["temperature"]),
                "pressure": float(s["pressure"]),
            }
            for s in samples
        ]
    }


@router.post("/dataset/random")
async def analyze_random():
    """Pick a random industrial sample from the dataset and run full analysis."""
    row, reading = get_random_sample()
    report = await analyze_gas(reading)
    return {
        "sample": {
            "id": int(row["id"]),
            "name": row["name"],
            "industry_type": row["industry_type"],
        },
        "report": report,
    }


@router.post("/dataset/analyze/{row_id}")
async def analyze_by_id(row_id: int):
    """Run analysis on a specific dataset entry by its ID (1–20)."""
    row = get_sample_by_id(row_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"No dataset entry with id={row_id}")
    reading = row_to_sensor_reading(row)
    report = await analyze_gas(reading)
    return {
        "sample": {
            "id": int(row["id"]),
            "name": row["name"],
            "industry_type": row["industry_type"],
        },
        "report": report,
    }
