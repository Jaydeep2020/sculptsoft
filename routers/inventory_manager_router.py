from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_session
from services.inventory_manager import InventoryManager
from models.inventory_model import InventoryModel
from schemas.inventory_schema import InventoryCreate
from services.generic import Generic

from auth.role_dependency import require_role
from models.enums import UserRole

router = APIRouter(
    prefix="/inventory-manager",
    tags = ["Inventory Operations"]
)


# Add Inventory
@router.post("/add_inventory", status_code=status.HTTP_201_CREATED)
def add_inventory(
        inventory: InventoryCreate,
        session: Session = Depends(get_session),
        current_user = Depends(
            require_role([UserRole.STAFF, UserRole.ADMIN])
        )
):
    try:
        inventory_model = InventoryModel(
            name = inventory.name,
            location = inventory.location
        )

        InventoryManager.add_inventory(
            session=session,
            inventory=inventory_model
        )

        return {
            "message": "Inventory added successfully"
        }

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))


# View all inventories
@router.get("/view_inventories", status_code=status.HTTP_200_OK)
def view_inventories(
        session: Session = Depends(get_session),
        current_user=Depends(
            require_role([UserRole.STAFF, UserRole.ADMIN])
        )
):
    inventories = InventoryManager.view_inventories(session=session)

    return inventories


# View total stock of product across all inventory
@router.get("/get_total_stock_across_inventories", status_code=status.HTTP_200_OK)
def get_total_stock_across_inventories(
        product_name: str,
        session: Session = Depends(get_session),
        current_user=Depends(
            require_role([UserRole.STAFF, UserRole.ADMIN])
        )
):
    try:

        product = InventoryManager.get_total_stock_across_inventories(session=session, product_name=product_name)

        return product

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete_inventory", status_code=status.HTTP_200_OK)
def delete_inventory(
        inventory_name: str,
        inventory_location: str,
        session: Session = Depends(get_session),
        current_user=Depends(
            require_role([UserRole.ADMIN])
        )
):
    try:

        InventoryManager.delete_inventory(
            session=session,
            name=inventory_name,
            location=inventory_location
        )

        return {
            "message": "Inventory deleted successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Transfer stocks from one inventory to another
@router.post("/transfer_stock/", status_code=status.HTTP_200_OK)
def transfer_stock(
        source_inventory_name: str,
        source_inventory_location: str,
        destination_inventory_name: str,
        destination_inventory_location: str,
        product_name: str,
        quantity: int,
        session: Session = Depends(get_session),
        current_user=Depends(
            require_role([UserRole.STAFF, UserRole.ADMIN])
        )
):
    try:

        source_inventory_id = Generic.get_inventory_id(inventory_name=source_inventory_name, inventory_location=source_inventory_location, session=session)
        destination_inventory_id = Generic.get_inventory_id(inventory_name=destination_inventory_name, inventory_location=destination_inventory_location, session=session)

        InventoryManager.transfer_stock(
            session=session,
            source_inventory_id=source_inventory_id,
            destination_inventory_id=destination_inventory_id,
            quantity=quantity,
            product_name=product_name,
        )

        return {
            "message": "Stock transferred successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
