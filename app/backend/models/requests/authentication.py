from datetime import datetime, timedelta

import jwt
from decouple import config
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

# Read from environment variables or set defaults
SECRET_KEY = config("SECRET_KEY", default="default_secret_key")
EXPIRE_TIME_MINUTE = config("EXPIRE_TIME_MINUTE", default=30)


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = SECRET_KEY

    def get_password_hash(self, password):
        """Generate a hashed password.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """Verify a plain text password against a hashed password.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, username, role):
        """Generate a JWT token.

        Args:
            username (str): The ID of the user.
            role (str): The role of the user.

        Returns:
            str: The encoded JWT token.
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=EXPIRE_TIME_MINUTE),
            "iat": datetime.utcnow(),
            "sub": username,
            "role": role,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        """Decode a JWT token.

        Args:
            token (str): The JWT token to decode.

        Raises:
            HTTPException: If the token is invalid or expired.

        Returns:
            tuple: The user ID and role extracted from the token.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"], payload["role"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """Extract user ID and role from the JWT token.

        Args:
            auth (HTTPAuthorizationCredentials, optional): The HTTP authorization credentials. Defaults to Security(security).

        Returns:
            dict: A dictionary containing the user ID and role.
        """
        username, list_of_roles = self.decode_token(auth.credentials)
        return {"username": username, "list_of_roles": list_of_roles}

    def encode_verification_token(self, username):
        """Generate a verification token.

        Args:
            username (str): The ID of the user.

        Returns:
            str: The encoded JWT token.
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=30),  # Token expires in 30 day
            "iat": datetime.utcnow(),
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_verification_token(self, token):
        """Decode a verification token.

        Args:
            token (str): The JWT token to decode.

        Raises:
            HTTPException: If the token is invalid or expired.

        Returns:
            str: The user ID extracted from the token.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]  # Return the username
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Verification token has expired"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid verification token")
