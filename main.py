from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Accessories", "in_stock": True},
    {"id": 2, "name": "USB-C Charger", "price": 899, "category": "Accessories", "in_stock": True},
    {"id": 3, "name": "Bluetooth Speaker", "price": 1499, "category": "Audio", "in_stock": True},
    {"id": 4, "name": "Phone Stand", "price": 299, "category": "Accessories", "in_stock": False},

    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 3499, "category": "Accessories", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1999, "category": "Electronics", "in_stock": True}
]

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):

    result = [p for p in products if p["category"] == category_name]

    if not result:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": result,
        "total": len(result)
    }

@app.get("/products/instock")
def get_instock_products():

    instock_items = [p for p in products if p["in_stock"] == True]

    return {
        "in_stock_products": instock_items,
        "count": len(instock_items)
    }


@app.get("/store/summary")
def store_summary():

    total_products = len(products)

    in_stock = len([p for p in products if p["in_stock"]])

    out_of_stock = len([p for p in products if not p["in_stock"]])

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }

@app.get("/products/deals")
def get_product_deals():

    best_deal = min(products, key=lambda x: x["price"])

    premium_pick = max(products, key=lambda x: x["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }
