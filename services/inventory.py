from unicodedata import category

from exceptions import ProductNotFoundException, InsufficientStockException
from services.generic import Generic
from models.product_model import ProductModel
from sqlalchemy.orm import Session
from models.inventory_stock_model import InventoryStockModel
from db.database import get_session

class Inventory:

    @staticmethod
    def add_product(session: Session, product: ProductModel, inventory_id: int, quantity: int):

        product_name = product.name

        # Check product in product table
        product_id = Generic.get_product_id(session, product_name)

        if product_id:

            # Check product already mapped to inventory
            check_if_exist = (
                session.query(InventoryStockModel)
                .filter(
                    InventoryStockModel.inventory_id == inventory_id,
                    InventoryStockModel.product_id == product_id
                )
                .first()
            )

            if check_if_exist:
                raise Exception(
                    f"Product {product_name} already exists in inventory. You can update the stock."
                )

        else:
            # Add new product only if not exists
            session.add(product)
            session.flush()

            product_id = product.id

        # Create inventory-product mapping
        ism = InventoryStockModel(
            product_id=product_id,
            inventory_id=inventory_id,
            quantity=quantity
        )

        session.add(ism)

        return product


    @staticmethod
    def delete_product_from_inventory(session: Session, product_name: str, inventory_id: int):

        product_id = Generic.get_product_id(session, product_name)

        if product_id is None:

            raise Exception(
                f"Product {product_name} does not exist in inventory."
            )

        inventory_stock = (
            session.query(InventoryStockModel)
            .filter(
                InventoryStockModel.inventory_id == inventory_id,
                InventoryStockModel.product_id == product_id
            )
            .first()
        )

        if inventory_stock is None:
            raise ProductNotFoundException(
                product_name=product_name,
                inventory_name=inventory_id
            )

        session.delete(inventory_stock)


    @staticmethod
    def delete_product(session, product_name: str):
        product_id = Generic.get_product_id(session, product_name)

        if product_id is None:
            raise Exception(
                f"Product {product_name} does not exist in inventory."
            )

        product = session.query(ProductModel).filter(ProductModel.id == product_id).first()

        session.delete(product)


    @staticmethod
    def view_products(session: Session, inventory_id: int):

        inventory_stock = (
            session.query(
                ProductModel.name, ProductModel.category, ProductModel.price, InventoryStockModel.quantity, ProductModel.warranty_month, ProductModel.expiry_date
            )
            .join(ProductModel)
            .filter(InventoryStockModel.inventory_id == inventory_id)
            .all()
        )

        return inventory_stock

    @staticmethod
    def search_product(session: Session, product_name: str, inventory_id: int):

        product = (
            session.query(
                ProductModel.name, ProductModel.category, ProductModel.price, InventoryStockModel.quantity
            )
            .join(ProductModel)
            .filter(InventoryStockModel.inventory_id == inventory_id,
                    ProductModel.name == product_name)
            .first()
        )

        if product is None:
            raise Exception(
                f"Product {product_name} does not exist in inventory."
            )

        return product

    @staticmethod
    def update_product(session: Session, product_name: str, inventory_id: int, quantity: int):


        product_id = Generic.get_product_id(session, product_name)

        if product_id is None:
            raise Exception(
                f"Product {product_name} does not exist in inventory."
            )

        product_stock = (
            session.query(InventoryStockModel)
            .filter(InventoryStockModel.inventory_id == inventory_id,
                    InventoryStockModel.product_id == product_id)
            .first()
        )

        if product_stock is None:
            raise Exception(f"Product {product_name} does not exist in inventory.")

        # # Update quantity
        # if quantity <= product_stock.quantity:
        #     raise Exception(f"Product {product_name} quantity is greater than stock quantity.")


        product_stock.quantity += quantity







from models.enums import CategoryType
#
# with get_session() as session:
#     products = Inventory.view_products(session, 1)
#     for i in products:
#         print(i)
#     inventory_id = Generic.get_inventory_id(session, 'Zepto', 'Bopal')
#     print(inventory_id)
#     p = ProductModel(name='laptop', category=CategoryType.ELECTRICAL, price=30000, warranty_month=6)
#     product = Inventory.add_product(session, p , inventory_id, 10)
#     print(product)
    # Inventory.delete_product(session, 'milk')
#
