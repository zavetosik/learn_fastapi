from pydantic import BaseModel, Field
from datetime import datetime


class CarPriceImageSchema(BaseModel):
    price: float = Field(ge=1)
    image: str = Field(examples=['https://upload.wikimedia.org/wikipedia/uk/1/18/I_Am_Legend_%28ukr_poster%29.jpg'])


class CarCreateSchema(CarPriceImageSchema):
    title: str = Field(examples=['M3 Competition'])
    brand: str = Field(examples=['BMW'])


class CarSavedSchema(CarCreateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)