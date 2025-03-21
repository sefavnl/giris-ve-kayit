from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
import secrets
import string

from .models import TokenData, UserInDB
from .database import get_user_by_email, store_password_reset_token, verify_password_reset_token, update_user, delete_password_reset_token

# JWT configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password utilities
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# User authentication
def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# JWT token utilities
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Password reset utilities
def generate_password_reset_token(length=32):
    """Generate a secure random token for password reset"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_password_reset(email: str):
    """Create a password reset token and store it"""
    # Check if user exists
    user = get_user_by_email(email)
    if not user:
        # Don't reveal if email exists or not for security
        return True
        
    # Generate token
    token = generate_password_reset_token()
    
    # Store token
    store_password_reset_token(email, token)
    
    return token

def reset_password(token: str, new_password: str):
    """Reset user password using the reset token"""
    # Verify token and get email
    email = verify_password_reset_token(token)
    if not email:
        return False
        
    # Hash the new password
    hashed_password = get_password_hash(new_password)
    
    # Update user password
    success = update_user(email, {"hashed_password": hashed_password})
    
    if success:
        # Delete the used token
        delete_password_reset_token(token)
        
    return success 