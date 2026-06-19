from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status


from schemas import CarCreateSchema, CarSavedSchema, CarPriceImageSchema
from settings import settings


class MongoDBStorage:
    def __init__(self):
        client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        db = client[settings.MONGO_DB]
        self.collection = db[settings.MONGO_COLLECTION]

    def create_car(self, car: CarCreateSchema) -> CarSavedSchema:
        car_dict = car.model_dump()
        car_dict['created_at'] = datetime.now()
        saved_car_in_db = self.collection.insert_one(car_dict)

        saved_car = self.get_car(saved_car_in_db.inserted_id)

        return saved_car

    def update_car(self, car_id: str, new_car_data: CarPriceImageSchema | CarCreateSchema) -> CarSavedSchema:
        payload = {'$set': new_car_data.model_dump()}
        result = self.collection.update_one(self._get_object_id_query(car_id), payload)
        if not result.raw_result['n']:
            raise HTTPException(
                detail=f'Book with id={car_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        saved_car = self.get_car(car_id)
        return saved_car

    def _get_object_id_query(self, car_id: str) -> dict[str, ObjectId]:
        try:
            query = {"_id": ObjectId(car_id)}
            return query
        except InvalidId:
            raise HTTPException(
                detail=f"Invalid book id {car_id}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def get_car(self, car_id: str) -> CarSavedSchema:
        car = self.collection.find_one(self._get_object_id_query(car_id))
        if not car:
            raise HTTPException(
                detail=f'Book with id={car_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        car = self.transform_car(car)

        return car

    def delete_car(self, car_id: str) -> None:
        self.get_car(car_id)
        self.collection.delete_one(self._get_object_id_query(car_id))

    def transform_car(self, car: dict) -> CarSavedSchema:
        car = CarSavedSchema(
            title=car['title'],
            image=car['image'],
            price=car['price'],
            brand=car['brand'],
            id=str(car['_id']),
            created_at=car['created_at'],
            year=car['year'],
            mileage=car['mileage'],
            color=car['color'],
        )
        return car


    def get_cars(self, q: str = "", page: int = 1)-> list[CarSavedSchema]:
        query = {}
        if q:
            query_words = q.split()
            print(query_words)

            query_words = [word.lower() for word in query_words if len(word) > 1]

            if query_words:
                query_words_dicts = [{'title': {"$regex": word, "$options": 'i'}} for word in query_words]
                query = {
                    "$and": query_words_dicts
                }
        skip = (page - 1) *  settings.PAGE_SIZE
        cars = self.collection.find(query).limit(settings.PAGE_SIZE).skip(skip)
        saved_cars = []
        for car in cars:
            saved_cars.append(self.transform_car(car))

        return saved_cars



storage = MongoDBStorage()
