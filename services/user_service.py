from sqlalchemy.orm import Session

from auth.jwt_handler import create_access_token
from models.enums import UserRole
from models.user_model import UserModel
from auth.password_handler import hash_password, verify_password

class UserService:

    @staticmethod
    def register_user(
            session: Session,
            username: str,
            email: str,
            password: str,
            role: UserRole
    ):
        existing_user = (
            session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

        if existing_user:
            raise Exception('User already exists')

        hashed_password = hash_password(password)

        user = UserModel(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role
        )

        session.add(user)

        # return user

    @staticmethod
    def login_user(
            session: Session,
            email: str,
            password: str
    ):

        user = (
            session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

        if not user:
            raise Exception('Invalid Email')

        if not verify_password(
            password,
            str(user.hashed_password)
        ):
            raise Exception('Invalid Password')

        access_token = create_access_token(
            data = {
                "sub": user.email,
                "role": user.role.value
            }
        )

        return access_token