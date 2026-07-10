from fastapi import APIRouter, status, Query
from new_schemas import AddRentalCarSchema, SavedRentalCarSchema

from new_storage import storage

api_router = APIRouter(
    prefix='/api/cars'
)

@api_router.post("", status_code=status.HTTP_201_CREATED)
def add_car(car: AddRentalCarSchema) -> SavedRentalCarSchema:
    saved_car = storage.add_car(car)

    return saved_car

@api_router.get('/get/car/{car_id}')
def get_car(car_id: str) -> SavedRentalCarSchema:
    saved_car = storage.get_car(car_id)

    return saved_car

@api_router.delete('/delete/car/{car_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: str) -> None:
    storage.delete_car(car_id)

