from fastapi import FastAPI

from routers.inventory_router import router as inventory_router
from routers.inventory_manager_router import router as inventory_manager_router

app = FastAPI(title="Inventory Management API")

app.include_router(inventory_manager_router)
app.include_router(inventory_router)

@app.get("/")
def home():
    return {
        "message": "Inventory Management System Running",
    }