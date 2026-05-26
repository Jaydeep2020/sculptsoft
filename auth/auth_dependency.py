from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from db.database import get_session
from models.user_model import UserModel
from sqlalchemy.orm import Session

SECRET_KEY = "inventory_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = (
            session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

        if user is None:

            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )