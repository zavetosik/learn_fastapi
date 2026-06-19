from fastapi import APIRouter, status, Query
from schemas import CarCreateSchema, CarSavedSchema, CarPriceImageSchema

from storage import storage

api_router = APIRouter(
    prefix='/api/cars'
)

@api_router.post("", status_code=status.HTTP_201_CREATED)
def create_car(car: CarCreateSchema) -> CarSavedSchema:
    saved_car = storage.create_car(car)

    return saved_car


@api_router.get("/{car_id}")
def get_car(car_id: str) -> CarSavedSchema:
    saved_car = storage.get_car(car_id)

    return saved_car


@api_router.get("")
def get_cars(
        page: int = Query(default=1, ge=1),
        q: str = Query(default=''),
) -> list[CarSavedSchema]:
    saved_cars = storage.get_cars(q, page=page)

    return saved_cars


@api_router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: str) -> None:
    storage.delete_car(car_id)


@api_router.patch("/{car_id}")
def patch_car(car_id: str, new_car_data: CarPriceImageSchema) -> CarSavedSchema:
    patched_car = storage.update_car(car_id, new_car_data)

    return patched_car


@api_router.put("/{car_id}")
def put_car(car_id: str, car: CarCreateSchema) -> CarSavedSchema:
    put_car_obj = storage.update_car(car_id, car)

    return put_car_obj