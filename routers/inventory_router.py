from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_session
# from main import warranty, expiry_date
from typing import List

from services.inventory import Inventory
from models.product_model import ProductModel
from schemas.product_schema import ProductCreate, ProductResponse
from schemas.inventory_schema import InventoryCreate
from services.generic import Generic

router = APIRouter(
    prefix="/inventory",
    tags=["Product Operations"]
)


# Add product in inventory
@router.post("/add_product")
def add_product(
        product: ProductCreate,
        inventory: InventoryCreate,
        quantity: int,
        session: Session = Depends(get_session)
):
    try:

        inventory_id = Generic.get_inventory_id(session, inventory.name, inventory.location)

        product_model = ProductModel(
            name=product.name,
            category=product.category,
            price=product.price,
            warranty_month=product.warranty_month,
            expiry_date=product.expiry_date
        )

        Inventory.add_product(
            session=session,
            product=product_model,
            inventory_id=inventory_id,
            quantity=quantity
        )

        return {
            "message": "Product added successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# View Products from inventory
@router.get("/view-products/", response_model=List[ProductResponse])
def view_products(
        name: str,
        location: str,
        session: Session = Depends(get_session)
):
    try:
        inventory_id = Generic.get_inventory_id(session, name, location)

        products = Inventory.view_products(
            session=session,
            inventory_id=inventory_id
        )

        return products

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#Search product in inventory
@router.get("/search_product", response_model=List[ProductResponse])
def search_products(
        product_name: str,
        inventory_name: str,
        inventory_location: str,
        session: Session = Depends(get_session)
):
    try:
        inventory_id = Generic.get_inventory_id(session, inventory_name, inventory_location)

        product = Inventory.search_product(
            session=session,
            product_name=product_name,
            inventory_id=inventory_id
        )

        return product

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update Product
@router.put("/update_product/")
def update_product(
        inventory_name: str,
        inventory_location: str,
        product_name: str,
        quantity: int,
        session: Session = Depends(get_session)
):
    try:
        inventory_id = Generic.get_inventory_id(session, inventory_name, inventory_location)

        Inventory.update_product(
            session=session,
            product_name=product_name,
            inventory_id=inventory_id,
            quantity=quantity
        )

        return {
            "message": "Product updated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# delete product from inventory
@router.delete("/delete_product_from_inventory/")
def delete_product_from_inventory(
        inventory_name: str,
        inventory_location: str,
        product_name: str,
        session: Session = Depends(get_session)
):
    try:
        inventory_id = Generic.get_inventory_id(session, inventory_name, inventory_location)

        Inventory.delete_product_from_inventory(
            product_name=product_name,
            inventory_id=inventory_id,
            session=session
        )
        return {
            "message": "Product deleted successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete Product Completely from all inventories
@router.delete("/delete_product/")
def delete_product(
        product_name: str,
        session: Session = Depends(get_session)
):
    try:
        Inventory.delete_product(
            session=session,
            product_name=product_name
        )
        return {
            "message": f"Product '{product_name}' deleted successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

