from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status


from new_schemas import AddRentalCarSchema, SavedRentalCarSchema
from new_settings import settings

class MongoDBStorage:
    def __init__(self):
        client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        db = client[settings.MONGO_DB]
        self.collection_cars = db[settings.MONGO_COLLECTION_CARS]
        self.collection_trucks = db[settings.MONGO_COLLECTION_TRUCKS]

    def transform_car(self, car: dict) -> SavedRentalCarSchema:
        car = SavedRentalCarSchema(
            type=car['type'],
            title=car['title'],
            brand=car['brand'],
            year=car['year'],
            mileage=car['mileage'],
            color=car['color'],
            id=str(car['_id']),
            created_at=car['created_at'],
        )
        return car

    def _get_object_id_query(self, car_id: str) -> dict[str, ObjectId]:
        try:
            query = {'_id': ObjectId(car_id)}
            return query
        except InvalidId:
            raise HTTPException(
                detail=f"Invalid car id {car_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def add_car(self, car: AddRentalCarSchema) -> SavedRentalCarSchema:
        car_dict = car.model_dump()
        car_dict['created_at'] = datetime.now()
        if car_dict['type'] == "Car":
            saved_car_in_db = self.collection_cars.insert_one(car_dict)
            saved_car = self.get_car(saved_car_in_db.inserted_id)
        elif car_dict['type'] == "Truck":
            saved_car_in_db = self.collection_trucks.insert_one(car_dict)
            saved_car = self.get_car(saved_car_in_db.inserted_id)
        return saved_car

    def get_car(self, car_id: str) -> SavedRentalCarSchema:
        query = self._get_object_id_query(car_id)

        car = self.collection_cars.find_one(query)
        if not car:
            car = self.collection_trucks.find_one(query)
        if not car:
            raise HTTPException(
                detail=f'Car with id={car_id} not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        car = self.transform_car(car)

        return car

    def delete_car(self, car_id: str) -> None:
        self.get_car(car_id)
        car = self.collection_cars.delete_one(self._get_object_id_query(car_id))
        if not car:
            self.collection_trucks.delete_one(self._get_object_id_query(car_id))


storage = MongoDBStorage()
