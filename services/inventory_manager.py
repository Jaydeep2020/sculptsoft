from models import ProductModel
from models.inventory_model import InventoryModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from services.generic import Generic
# from db.database import get_session
from models.inventory_stock_model import InventoryStockModel

class InventoryManager:

    @staticmethod
    def add_inventory(session: Session, inventory: InventoryModel):

        inventory_id = Generic.get_inventory_id(session, inventory.name, inventory.location)

        if inventory_id is None:
            session.add(inventory)

        else:
            raise Exception(
                f"Inventory '{inventory.name}' with '{inventory.location}' location already exists"
            )

    @staticmethod
    def view_inventories(session: Session):

        inventories = session.query(InventoryModel).all()

        return inventories

    @staticmethod
    def delete_inventory(session: Session, name: str, location: str):

        inventory = (
            session.query(InventoryModel)
            .filter(InventoryModel.name == name,
                    InventoryModel.location == location)
            .one_or_none()
        )

        if inventory is None:
            raise Exception(f"Inventory '{name}' with '{location}' location does not exist")

        session.delete(inventory)

    @staticmethod
    def get_total_stock_across_inventories(session: Session, product_name: str):

        product = (
            session.query(
                ProductModel.name, ProductModel.category, func.sum(InventoryStockModel.quantity).label("total_stocks")
            )
            .join(InventoryStockModel)
            .filter(ProductModel.name == product_name)
            .group_by(ProductModel.name, ProductModel.category)
            .first()
        )

        return product


    @staticmethod
    def transfer_stock(session: Session, product_name: str, source_inventory_id: int, destination_inventory_id: int, quantity: int):

        if quantity <= 0:
            raise Exception("Transfer quantity must be greater than 0")

        if source_inventory_id == destination_inventory_id:
            raise Exception(f"Source and destination inventories cannot be the same")

        product_id = Generic.get_product_id(session, product_name)

        if product_id is None:
            raise Exception(f"Product '{product_name}' does not exist")

        # Get source inventory stock
        source_stock = (
            session.query(InventoryStockModel)
            .filter(InventoryStockModel.inventory_id == source_inventory_id,
                    InventoryStockModel.product_id == product_id
            )
            .first()
        )
        if source_stock is None:
            raise Exception(
                f"Product '{product_name}' does not exist in source inventory"
            )

        # Check sufficient stock
        if source_stock.quantity < quantity:
            raise Exception(
                f"Insufficient stock for '{product_name}'. "
                f"Available: {source_stock.quantity}, Required: {quantity}"
            )

        # Deduct from source inventory
        source_stock.quantity -= quantity

        # send update query immediately
        session.flush()

        # Get destination stock
        destination_stock = (
            session.query(InventoryStockModel)
            .filter(
                InventoryStockModel.inventory_id == destination_inventory_id,
                InventoryStockModel.product_id == product_id
            )
            .first()
        )

        # Update destination stock if exists
        if destination_stock:
            destination_stock.quantity += quantity

        # Else Insert new stock entry
        else:
            new_stock = InventoryStockModel(product_id=product_id,  inventory_id = destination_inventory_id, quantity=quantity)
            session.add(new_stock)










# im = InventoryModel(name='Zepto', location='Bopal')

# from db.database import get_session
# with get_session() as session:
#     inventories = InventoryManager.view_inventories(session)
#
#     for i in inventories:
#         print(i)



