from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum as SQLEnum
from models.enums import UserRole
from models.base import Base

class UserModel(Base):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role"), nullable=False, default=UserRole.STAFF)
