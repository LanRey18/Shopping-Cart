from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel  
from pydantic.dataclasses import dataclass


app = FastAPI()
templates = Jinja2Templates(directory="templates")

items = [
            {"prodId": 1, "name": "Sunscreen", "quantity" : 100, "price" : 10.99},
            {"prodId": 2, "name": "Facial Cleanser", "quantity" : 100, "price" : 15.59},
            {"prodId": 3, "name": "Niacininamide Serum", "quantity" : 100, "price" : 20},
            {"prodId": 4, "name": "Hyaluronic acid", "quantity" : 100, "price" :29.99},
            {"prodId": 5, "name": "Moisturizer", "quantity" : 100, "price" : 15.99},
            {"prodId": 6, "name": "Vitamin C Serum", "quantity" : 100, "price" : 15},
            {"prodId": 7, "name": "Toner", "quantity" : 100, "price" : 9.99},
            {"prodId": 8, "name": "Retinol", "quantity" : 100, "price" : 24.99},
        ]

orders = []


class Item(BaseModel):
    prodId: int 
    name: str 
    quantity: int 
    price: int 

class OrderRequest(BaseModel):
    prodId: int 
    quantity: int 

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})

@app.get("/items")
async def get_items(request: Request ):
    return templates.TemplateResponse("ViewItems.html", {"request": request,  "items": items})

@app.post("/create_item")
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
                return RedirectResponse("/", status_code=303) 
            # {"message": "Order successful", "orders": orders, "items" : items}
            else:
                return {"error": "Insufficient quantity available"}

    return {"error": "Item not found"}

@app.get("/orders")
def get_items(request: Request):
    return templates.TemplateResponse("Orders.html", {"request": request,  "orders": orders})