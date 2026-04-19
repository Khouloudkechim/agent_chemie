from pydantic import BaseModel, Field, model_validator

class GasComposition(BaseModel):
    CO: float = Field(default=0.0, ge=0.0, le=100.0)
    CH4: float = Field(default=0.0, ge=0.0, le=100.0)
    H2: float = Field(default=0.0, ge=0.0, le=100.0)
    SO2: float = Field(default=0.0, ge=0.0, le=100.0)
    CO2: float = Field(default=0.0, ge=0.0, le=100.0)
    H2S: float = Field(default=0.0, ge=0.0, le=100.0)
    N2: float = Field(default=0.0, ge=0.0, le=100.0)
    C3H8: float = Field(default=0.0, ge=0.0, le=100.0)

    @model_validator(mode='after')
    def check_sum(self) -> 'GasComposition':
        total = sum([self.CO, self.CH4, self.H2, self.SO2, self.CO2, self.H2S, self.N2, self.C3H8])
        if not (99.0 <= total <= 101.0):
            raise ValueError(f"Gas composition percentages must sum to ~100%, got {total}%")
        return self

class SensorReading(BaseModel):
    composition: GasComposition
    flow_rate: float = Field(..., gt=0, description="Volume flow rate in m3/h")
    temperature: float = Field(..., description="Temperature in Celsius")
    pressure: float = Field(..., gt=0, description="Pressure in bar")
