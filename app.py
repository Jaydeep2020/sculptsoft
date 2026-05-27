from fastapi import FastAPI

from routers.inventory_router import router as inventory_router
from routers.inventory_manager_router import router as inventory_manager_router
from routers.auth_router import router as auth_router

app = FastAPI(title="Inventory Management API")

app.include_router(inventory_manager_router)
app.include_router(inventory_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Inventory Management System Running",
    }