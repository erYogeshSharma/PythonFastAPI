from datetime import datetime, timedelta
from jose import JWTError, jwt

# required params -> SECRET_KEY, ALGORITHM :HS256, EXPIRE_TIME

SECRET_KEY = "035asdfkkam(sfao3490ri#w90fj34n9#_inv9udvj$34qen"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):

    to_encode = data.copy()  # copy the data

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # update the data with the expire time

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
