from db.base import Base
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class InventoryModel(Base):

    __tablename__ = 'inventory'

    __table_args__ = (
        UniqueConstraint("name", "location", name="unique_inventory"),
    )

    name : Mapped[str] = mapped_column(String(100), nullable=False)
    location : Mapped[str] = mapped_column(String(100), nullable=False)

    inventory_stocks = relationship("InventoryStockModel", back_populates="inventory")

    def __repr__(self):
        return (
            f"InventoryModel("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"location='{self.location}')"
        )