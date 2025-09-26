from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure password context with bcrypt settings
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Specify bcrypt rounds
    bcrypt__ident="2b",  # Use bcrypt 2b format
    bcrypt__min_rounds=4   # Minimum round
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        # First try bcrypt verification
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        # If bcrypt fails, try SHA256 verification (fallback hash)
        try:
            import hashlib
            expected_hash = hashlib.sha256(plain_password.encode()).hexdigest()
            if expected_hash == hashed_password:
                print(f"SHA256 password verification successful")
                return True
            else:
                print(f"SHA256 password verification failed")
                return False
        except Exception as sha_error:
            print(f"SHA256 verification error: {sha_error}")
            return False

def get_password_hash(password: str) -> str:
    """Hash a password."""
    try:
        # Ensure password is not too long for bcrypt (72 bytes max)
        if len(password.encode('utf-8')) > 72:
            password = password[:72]  # Truncate if too long
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        # Fallback to simple hash if bcrypt fails
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    # Use secret key from environment variable
    secret_key = os.getenv("SECRET_KEY", "fallback-secret-key")
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get the current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Use secret key from environment variable
        secret_key = os.getenv("SECRET_KEY", "fallback-secret-key")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception
    return {"user_id": user.id, "email": user.email}