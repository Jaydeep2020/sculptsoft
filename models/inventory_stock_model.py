from sqlalchemy import Integer, ForeignKey, UniqueConstraint, CheckConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

class InventoryStockModel(Base):

    __tablename__ = 'inventory_stock'

    __table_args__ = (
        UniqueConstraint('inventory_id', 'product_id', name='unique_inventory_product'),
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
    )

    inventory_id : Mapped[int] = mapped_column(ForeignKey('inventory.id', ondelete="CASCADE", onupdate="CASCADE", name='fk_inventory'), nullable=False)
    product_id : Mapped[int] = mapped_column(ForeignKey('product.id', ondelete="CASCADE", onupdate="CASCADE", name='fk_product'), nullable=False)

    quantity : Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    inventory = relationship("InventoryModel", back_populates="inventory_stocks")
    product = relationship("ProductModel", back_populates="inventory_stocks")