from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class AddRentalCarSchema(BaseModel):
    type: Literal["Car", "Truck"] = Field(examples=['Car'])
    title: str = Field(examples=['Porsche 911 GT 3'])
    brand: str = Field(examples=['Porsche'])
    year: int = Field(ge=1900,le=2026,examples=[2026])
    mileage: int = Field(ge=1,examples=[31843])
    color:  str = Field(examples=['blue'])

class SavedRentalCarSchema(AddRentalCarSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
 