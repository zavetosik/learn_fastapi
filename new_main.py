from fastapi import FastAPI
from new_api_router import api_router

app = FastAPI(
    title='Car rental'
)


app.include_router(api_router, tags=['CARS'])