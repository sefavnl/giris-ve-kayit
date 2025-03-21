from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .models import UserCreate, Token, PasswordResetRequest, PasswordReset, UserResponse, UserLogin
from .auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user, 
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_password_reset,
    reset_password
)
from .database import add_user, get_user_by_email

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    # Check if user already exists
    db_user = get_user_by_email(user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    user_data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "hashed_password": hashed_password
    }
    
    created_user = add_user(user_data)
    
    return {
        "id": created_user["id"],
        "email": created_user["email"],
        "first_name": created_user["first_name"],
        "last_name": created_user["last_name"]
    }

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin):
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "first_name": current_user["first_name"],
        "last_name": current_user["last_name"]
    }

# Password Reset Endpoints
@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(request: PasswordResetRequest):
    """Request a password reset email"""
    token = create_password_reset(request.email)
    
    # In a real-world app, you would send an email with a link like:
    # https://yourfrontend.com/reset-password?token={token}
    
    # For demo purposes, just return the token
    return {"message": "If your email is registered, you will receive a password reset link.", "token": token}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def process_password_reset(reset_data: PasswordReset):
    """Process a password reset request with token"""
    if not reset_password(reset_data.token, reset_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token"
        )
    
    return {"message": "Password has been reset successfully"} 