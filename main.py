from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel  

app = FastAPI()
templates = Jinja2Templates(directory="templates")

items = []
orders = []

class Item(BaseModel):
    prodId: int = None
    name: str = None
    price: int = None
    quantity: int = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})

@app.get("/items")
def get_items(request: Request):
    return templates.TemplateResponse("ViewItems.html", {"request": request})

@app.post("/items")
def add_item(item : Item):
    items.append(item)
    return items

@app.post("/order")
def order_item(prodId : int ):
    orders.append(items[prodId])
    return orders