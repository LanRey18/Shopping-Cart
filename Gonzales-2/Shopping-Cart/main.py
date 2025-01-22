from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items = []

class Item(BaseModel):
    name: str = None
    quantity: int = None


@app.get("/")

async def root():
    return 'Hello to Russells Sari-Sari Store'

@app.get("/items")
def get_items():
    return items

@app.post("/items/")
def add_item(item : Item):
    items.append(item)
    return items