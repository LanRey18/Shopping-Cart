from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items = []
orders = []

class Item(BaseModel):
    prodId: int = None
    name: str = None
    price: int = None
    quantity: int = None


@app.get("/")

async def root():
    return "Hello to Russell's Sari-Sari Store"

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def add_item(item : Item):
    items.append(item)
    return items

@app.post("/orders")
def order_item(prodId : int ):
    orders.append(items[prodId])
    return orders