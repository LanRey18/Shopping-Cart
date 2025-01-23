from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel  

app = FastAPI()
templates = Jinja2Templates(directory="templates")

items = [
            {"prodId": 1, "name": "Apple", "quantity" : 5, "price" : 22},
            {"prodId": 2, "name": "Orange", "quantity" : 5, "price" : 22},
            {"prodId": 3, "name": "Grapes", "quantity" : 5, "price" : 22},
            {"prodId": 4, "name": "Grapes", "quantity" : 5, "price" : 22},
        ]
orders = []

class Item(BaseModel):
    prodId: int = None
    name: str = None
    quantity: int = None
    price: int = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})

@app.get("/items")
def get_items(request: Request):
    return templates.TemplateResponse("ViewItems.html", {"request": request,  "items": items})

@app.post("/items")
def add_item(item : Item):
    items.append(item)
    return items

@app.post("/order")
def order_item(prodId : int ):
    orders.append(items[prodId])
    return orders