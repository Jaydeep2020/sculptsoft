import enum

class CategoryType(enum.Enum):
    GROCERY = "GROCERY"
    ELECTRICAL = "ELECTRICAL"


class TransactionType(enum.Enum):
    ADD = "ADD"
    REMOVE = "REMOVE"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"