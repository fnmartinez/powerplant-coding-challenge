from typing import Optional, List
from pydantic import BaseModel, Field


class FuelsCosts(BaseModel):
    gas: Optional[float] = Field(None, alias='gas(euro/MWh)')
    kerosene: Optional[float] = Field(None, alias='kerosine(euro/MWh)')
    co2: Optional[int] = Field(None, alias='co2(euro/ton)')
    wind: Optional[int] = Field(None, alias='wind(%)')


class PowerPlantData(BaseModel):
    name: Optional[str]
    type: Optional[str]
    efficiency: Optional[float]
    pmin: Optional[int]
    pmax: Optional[int]


class PowerLoad(BaseModel):
    load: Optional[int]
    fuels: Optional[FuelsCosts]
    powerplants: Optional[List[PowerPlantData]]


class UnitCommitment(BaseModel):
    name: Optional[str]
    p: Optional[int]
