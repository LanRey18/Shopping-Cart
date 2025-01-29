from fastapi import FastAPI, Request, Form
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

orders = [
            {"prodId": 1, "name": "Apple", "quantity" : 2, "price" : 22},
         ]

class Item(BaseModel):
    prodId: int = None
    name: str = None
    quantity: int = None
    price: int = None

class OrderRequest(BaseModel):
    prodId: int
    quantity: int 

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
def order_item(order_request: OrderRequest):
    prodId = order_request.prodId
    quantity = order_request.quantity

    # Find the item in the items list
    for item in items:
        if item["prodId"] == prodId:
            # Check if there is enough quantity to order
            if item["quantity"] >= quantity:
                item["quantity"] -= quantity

                for order in orders:
                    if order["prodId"] == prodId:
                        order["quantity"] += quantity
                        order["price"] = item["price"] * order["quantity"]
                        return {"message": "Order successful", "orders": orders}

                # Add the ordered item to the orders list
                ordered_item = {
                    "prodId": item["prodId"],
                    "name": item["name"],
                    "quantity": quantity,
                    "price": item["price"] * quantity
                }
                orders.append(ordered_item)
                return {"message": "Order successful", "order": ordered_item}
            else:
                return {"error": "Insufficient quantity available"}

    return {"error": "Item not found"}

@app.get("/orders")
def get_items(request: Request):
    return templates.TemplateResponse("Orders.html", {"request": request,  "orders": orders})