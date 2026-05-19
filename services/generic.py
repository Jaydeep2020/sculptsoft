from sqlalchemy.orm import Session
from models.product_model import ProductModel
from models.inventory_model import InventoryModel

class Generic:

    @staticmethod
    def get_inventory_id(session: Session, inventory_name: str, inventory_location: str) -> int | None:

        inventory_record = session.query(InventoryModel).filter(InventoryModel.name == inventory_name, InventoryModel.location == inventory_location).first()

        return inventory_record.id if inventory_record else None


    @staticmethod
    def get_product_id(session: Session, product_name: str) -> int | None:

        product_record = session.query(ProductModel).filter(ProductModel.name == product_name).first()

        return product_record.id if product_record else None

