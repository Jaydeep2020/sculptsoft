from abc import ABC, abstractmethod
from exceptions import InsufficientStockException
from logs.logger_config import get_logger
from models.enums import CategoryType

logger = get_logger(__name__)

class Product(ABC):

    def __init__(self, name: str, quantity: int, price: float, category):
        self.__name = name
        self.__quantity = quantity
        self.__price = price
        self.__category = category

    # Getters (read-only for some)
    @property
    def name(self):
        return self.__name

    @property
    def quantity(self):
        return self.__quantity

    @property
    def price(self):
        return self.__price

    @property
    def category(self):
        return self.__category

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            logger.error(f"Invalid quantity update attempt for {self.name}: {value}")
            raise ValueError("Quantity cannot be negative")
        logger.info(f"Quantity updated | {self.name}: {self.quantity} -> {value}")
        self.quantity = value

    @price.setter
    def price(self, value):
        if value < 0:
            logger.error(f"Invalid price update attempt for {self.name}: {value}")
            raise ValueError("Price cannot be negative")
        logger.info(f"Price updated | {self.name}: {self.price} -> {value}")
        self.price = value

    def increase_stock(self, amount: int):
        if amount <= 0:
            logger.error(f"Invalid stock increase attempt for {self.name}: {amount}")
            raise ValueError("Stock Quantity cannot be negative")
        old_qty = self.quantity
        self.quantity += amount

        logger.info(
            f"Stock increased | {self.name}: {old_qty} -> {self.quantity} (+{amount})"
        )

    def decrease_stock(self, amount: int):
        if amount <= 0:
            logger.error(f"Invalid stock decrease attempt for {self.name}: {amount}")
            raise ValueError("Amount must be positive")

        if amount > self.quantity:
            logger.warning(
                f"Insufficient stock | {self.name}: Requested={amount}, Available={self.quantity}"
            )
            raise InsufficientStockException(self.name, amount, self.quantity)

        old_qty = self.quantity
        self.quantity -= amount

        logger.info(
            f"Stock decreased | {self.name}: {old_qty} -> {self.quantity} (-{amount})"
        )

    def is_available(self, required_quantity: int) -> bool:
        if required_quantity > self.quantity:
            logger.warning(
                f"Stock check failed | {self.name}: Required={required_quantity}, Available={self.quantity}"
            )
            raise InsufficientStockException(
                self.name, required_quantity, self.quantity
            )

        logger.debug(
            f"Stock available | {self.name}: Required={required_quantity}, Available={self.quantity}"
        )
        return True

    # The single abstract method – each subclass must implement its own tax calculation
    @abstractmethod
    def calculate_tax(self) -> float:
        """Return the tax amount for this product (based on product-specific rules)."""
        pass

    def __str__(self):
        return f"""
Product : {self.name}
Quantity: {self.quantity}
Price: {self.price}
Category: {self.category}"""


# ---------- SUBCLASS: ELECTRICAL PRODUCT ----------
class GroceryProduct(Product):
    def __init__(self, name: str, quantity: int, price: float, expiry_date: str):
        super().__init__(name, quantity, price, category=CategoryType.GROCERY)
        self._expiry_date = expiry_date
        logger.info(f"Grocery product initialized: (Name: {self.name} | Qty: {self.quantity} | Category: {self.category} | Price: {self.price} | Expiry: {self._expiry_date})")

    @property
    def expiry_date(self):
        return self._expiry_date

    # Implement the abstract method: groceries may have a lower tax rate (e.g., 5%)
    def calculate_tax(self) -> float:
        tax = self.price * 0.05
        logger.debug(f"Tax calculated (Grocery) | {self.name}: {tax}")
        return tax

    # Polymorphism: override __str__ to include expiry date
    def __str__(self):
        return super().__str__() + f"\nExpiry Date: {self._expiry_date}\nTax: {self.calculate_tax():.2f}"

# ---------- SUBCLASS: ELECTRICAL PRODUCT ----------
class ElectricalProduct(Product):
    def __init__(self, name: str, quantity: int, price: float, warranty_period: int):
        super().__init__(name, quantity, price, category=CategoryType.ELECTRICAL)
        self._warranty_period = warranty_period
        logger.info(
            f"Electrical product initialized | Warranty: {self._warranty_period} months"
        )

    @property
    def warranty_period(self):
        return self._warranty_period

    # Implement the abstract method: electrical products may have a higher tax rate (e.g., 18%)
    def calculate_tax(self) -> float:
        tax = self.price * 0.18
        logger.debug(f"Tax calculated (Electrical) | {self.name}: {tax}")
        return tax


    # Polymorphism: override __str__ to include warranty period
    def __str__(self):
        return super().__str__() + f"\nWarranty Period: {self._warranty_period}\nTax: {self.calculate_tax():.2f}"

# p = ElectricalProduct(name="laptop", quantity=100, price=100, warranty_period=1)
#
# print(p)