import csv
import random
import os
from models.gas_input import SensorReading, GasComposition

# Path to the CSV dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "industrial_dataset.csv")

def _load_dataset() -> list[dict]:
    rows = []
    with open(DATASET_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

# Load once at module import time
_DATASET = _load_dataset()

def get_all_samples() -> list[dict]:
    """Return all rows as raw dicts (for listing)."""
    return _DATASET

def get_sample_by_id(row_id: int) -> dict | None:
    """Return a single row by its 1-based id."""
    for row in _DATASET:
        if int(row["id"]) == row_id:
            return row
    return None

def row_to_sensor_reading(row: dict) -> SensorReading:
    """Convert a CSV row into a SensorReading model."""
    return SensorReading(
        composition=GasComposition(
            SO2=float(row.get("SO2", 0)),
            H2S=float(row.get("H2S", 0)),
            CO=float(row.get("CO", 0)),
            CO2=float(row.get("CO2", 0)),
            N2=float(row.get("N2", 0)),
            CH4=float(row.get("CH4", 0)),
        ),
        flow_rate=float(row.get("flow_rate", 1000)),
        temperature=float(row.get("temperature", 100)),
        pressure=float(row.get("pressure", 1.0)),
    )

def get_random_sample() -> tuple[dict, SensorReading]:
    """Pick a random row and return (raw_row, SensorReading)."""
    row = random.choice(_DATASET)
    return row, row_to_sensor_reading(row)
