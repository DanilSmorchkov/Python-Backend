from fastapi import FastAPI
from hw_2_RESTAPI_and_3_docker.app.item_router import item_router
from hw_2_RESTAPI_and_3_docker.app.cart_router import cart_router

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.include_router(item_router)
app.include_router(cart_router)
Instrumentator().instrument(app).expose(app)
