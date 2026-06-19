from pydantic import BaseModel, Field
from datetime import datetime


class CarPriceImageSchema(BaseModel):
    price: float = Field(ge=1)
    image: str = Field(examples=['https://drivar.de/wp-6401f-content/uploads/2022/10/i9xC4cjstBAayPPzgbMir-scaled.webp'])


class CarCreateSchema(CarPriceImageSchema):
    title: str = Field(examples=['M3 Competition'])
    brand: str = Field(examples=['BMW'])
    year: int = Field(examples=[2022])
    mileage: int = Field(examples=[4])


class CarSavedSchema(CarCreateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)