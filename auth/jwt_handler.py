from jose import jwt
from jose import JWTError

from datetime import datetime, timedelta, timezone

SECRET_KEY = "inventory_secret_key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):

    """
    Create JWT access token for authenticated users.

    This function:
    - copies user payload data
    - adds token expiration time
    - encodes payload into JWT token
    - returns encoded JWT string

    Args:
        data (dict):
            Payload data to store inside token.
            Usually contains user identity like:
            {
                "sub": "user@example.com"
                "role": "ADMIN"
            }

    Returns:
        str:
            Encoded JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt