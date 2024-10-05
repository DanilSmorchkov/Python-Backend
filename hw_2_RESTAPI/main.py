from fastapi import FastAPI
from .app.item_router import item_router
from .app.cart_router import cart_router

app = FastAPI()
app.include_router(item_router)
app.include_router(cart_router)
