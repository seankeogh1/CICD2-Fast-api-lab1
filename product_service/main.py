from fastapi import FastAPI,HTTPException

app = FastAPI(title="Product Service")

PRODUCTS ={
    1:{"id": 1, "name": "laptop", "price": 899},
    2:{"id": 2, "name": "Mousee", "price":25.0}
}

@app.get("/products/{product_id}") 
def get_product(product_id: int): 
    product = PRODUCTS.get(product_id) 
    if product is None: 
        raise HTTPException(status_code=404, detail="Product not found") 
    return product 