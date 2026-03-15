from fastapi import FastAPI, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Accessories", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Phone Stand", "price": 299, "category": "Accessories", "in_stock": False},
]

cart = []
orders = []
order_counter = 1


@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}


@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f'{product["name"]} is out of stock')

    # update quantity if item already exists
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["unit_price"] * item["quantity"]

            return {
                "message": "Cart updated",
                "cart_item": item
            }

    cart_item = {
        "product_id": product["id"],
        "product_name": product["name"],
        "unit_price": product["price"],
        "quantity": quantity,
        "subtotal": product["price"] * quantity
    }

    cart.append(cart_item)

    return {
        "message": "Added to cart",
        "cart_item": cart_item
    }


@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": f'{item["product_name"]} removed from cart'}

    raise HTTPException(status_code=404, detail="Item not found in cart")


@app.post("/cart/checkout")
def checkout(customer_name: str, delivery_address: str):

    global order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    created_orders = []

    for item in cart:
        order = {
            "order_id": order_counter,
            "customer_name": customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"],
            "delivery_address": delivery_address
        }

        orders.append(order)
        created_orders.append(order)
        order_counter += 1

    cart.clear()

    return {
        "orders_placed": len(created_orders),
        "orders": created_orders
    }


@app.get("/orders")
def get_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            orders.remove(order)
            return {"message": f"Order {order_id} deleted successfully"}

    raise HTTPException(status_code=404, detail="Order not found")
