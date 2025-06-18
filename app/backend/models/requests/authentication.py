from decouple import config

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Read from environment variables or set defaults
SECRET_KEY = config("SECRET_KEY", default="default_secret_key")
EXPIRE_TIME_MINUTE = config("EXPIRE_TIME_MINUTE", default=30)

class AuthHandler:

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = SECRET_KEY

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id, role):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=EXPIRE_TIME_MINUTE),
            "iat": datetime.utcnow(),
            "sub": user_id,
            "role": role
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"], payload["role"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        user_id, role = self.decode_token(auth.credentials)
        return {"user_id": user_id, "role": role}
    

    def encode_verification_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=30),  # Token expires in 30 day
            "iat": datetime.utcnow(),
            "sub": user_id
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_verification_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]  # Return the user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Verification token has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid verification token")