from pydantic import BaseModel
from typing import List

class PlotRequest(BaseModel):
    mz: str
    intensity: str
