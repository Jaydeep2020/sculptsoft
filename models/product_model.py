from decimal import Decimal
from datetime import date
from db.base import Base
from sqlalchemy import String, Numeric, Enum as SQLEnum, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .enums import CategoryType


class ProductModel(Base):

    __tablename__ = "product"

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_product_price_positive"),
        CheckConstraint("warranty_month >= 0", name="check_product_warranty_month_positive"),
    )

    name : Mapped[str] = mapped_column(String(100), nullable=False)
    category : Mapped[CategoryType] = mapped_column(SQLEnum(CategoryType, name="category_type"), nullable=False)
    price : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    expiry_date : Mapped[date | None] = mapped_column(Date, nullable=True)
    warranty_month : Mapped[int | None] = mapped_column(nullable=True)

    inventory_stocks = relationship("InventoryStockModel", back_populates="product")

