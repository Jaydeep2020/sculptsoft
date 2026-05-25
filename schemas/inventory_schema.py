from pydantic import BaseModel

class InventoryCreate(BaseModel):

    name: str
    location: str

class AddProductRequest(BaseModel):

    inventory_id: int
    quantity: int