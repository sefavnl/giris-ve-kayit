from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime, timedelta

# MongoDB connection string from environment variable
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://nozkanca7:sgshcoNN21@cluster0.ipznc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Create a MongoDB client
client = MongoClient(MONGO_URI)

# Get database and collections
db = client.user_auth_db
users_collection = db.users
password_reset_collection = db.password_reset_tokens

# Helper functions
def user_helper(user) -> dict:
    """Convert MongoDB user to dict"""
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "hashed_password": user["hashed_password"]
    }

# User database operations
def add_user(user_data: dict) -> dict:
    """Add a new user to the database"""
    user = users_collection.insert_one(user_data)
    new_user = users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

def get_user_by_email(email: str) -> dict:
    """Get a user by email"""
    user = users_collection.find_one({"email": email})
    if user:
        return user_helper(user)
    return None

def update_user(email: str, data: dict):
    """Update a user"""
    if len(data) < 1:
        return False
    user = users_collection.find_one({"email": email})
    if user:
        updated_user = users_collection.update_one(
            {"email": email}, {"$set": data}
        )
        if updated_user:
            return True
    return False

# Password reset operations
def store_password_reset_token(email: str, token: str):
    """Store a password reset token"""
    # Delete any existing tokens for this user
    password_reset_collection.delete_many({"email": email})
    
    # Create new token with expiry time (24 hours)
    expires = datetime.utcnow() + timedelta(hours=24)
    
    # Store the token
    password_reset_collection.insert_one({
        "email": email,
        "token": token,
        "expires": expires
    })
    return True

def verify_password_reset_token(token: str):
    """Verify if a password reset token is valid"""
    token_data = password_reset_collection.find_one({"token": token})
    
    if not token_data:
        return None
        
    # Check if token is expired
    if token_data["expires"] < datetime.utcnow():
        # Delete expired token
        password_reset_collection.delete_one({"_id": token_data["_id"]})
        return None
        
    return token_data["email"]

def delete_password_reset_token(token: str):
    """Delete a password reset token after it's been used"""
    password_reset_collection.delete_one({"token": token})
    return True 