from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_session

from fastapi.security import OAuth2PasswordRequestForm

from schemas.user_schema import (UserRegister, UserLogin, TokenResponse)

from services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Register User
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user: UserRegister,
        session: Session = Depends(get_session)
):
    try:
        UserService.register_user(
            session=session,
            username=user.username,
            email=user.email,
            password=user.password,
            role=user.role
        )

        return {
            "message": "User registered successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# code for Login with Swagger
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    try:

        token = UserService.login_user(
            session=session,
            email=form_data.username,
            password=form_data.password
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



# # Login User
# @router.post("/login", response_model=TokenResponse)
# def login_user(
#         user: UserLogin,
#         session: Session = Depends(get_session)
# ):
#     try:
#         token = UserService.login_user(
#             session=session,
#             email=user.email,
#             password=user.password
#         )
#
#         return {
#             "access_token": token,
#             "token_type": "bearer"
#         }
#
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))