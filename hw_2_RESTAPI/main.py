from fastapi import FastAPI
from hw_2_RESTAPI.app.item_router import item_router

app = FastAPI()
app.include_router(item_router)
