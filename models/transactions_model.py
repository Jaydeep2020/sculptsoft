from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, ForeignKey, Enum as SQLEnum, CheckConstraint
from models.base import Base
from models.enums import TransactionType

class TransactionsModel(Base):

    __tablename__ = "transactions"

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
    )

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='SET NULL', onupdate='CASCADE', name='fk_transaction_product'), nullable=False)

    source_inventory_id: Mapped[int | None] = mapped_column(ForeignKey('inventory.id', onupdate='CASCADE', ondelete='SET NULL', name='fk_source_inventory'), nullable=True)
    destination_inventory_id: Mapped[int | None] = mapped_column(ForeignKey('inventory.id', onupdate='CASCADE', ondelete='SET NULL', name='fk_destination_inventory'), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType, name="transaction_type"), nullable=False)

    # Relationships
    product = relationship("ProductModel")
    source_inventory = relationship("InventoryModel", foreign_keys=[source_inventory_id])
    destination_inventory = relationship("InventoryModel", foreign_keys=[destination_inventory_id])