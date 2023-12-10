from fastapi import FastAPI, HTTPException, Path
from pymongo import MongoClient
from datetime import datetime
from models import *
from bson import ObjectId

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb+srv://doadmin:tx95lEv0V426e83y@db-mongodb-blr1-29522-6758ad8a.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-blr1-29522")
db = client["social_media_db"]

# MongoDB collections
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]
likes_collection = db["likes"]
follows_collection = db["follows"]

print(db.users_collection.find_one({"username": "vishalg"}))

# Sample CRUD operation for creating a new user
@app.post("/users/create", response_model=User)
async def create_user(user: User):
    user_dict = user.dict()
    user_dict["created_at"] = datetime.utcnow()
    result = users_collection.insert_one(user_dict)
    print(result)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict

# Read User Endpoint
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str = Path(..., title="The ID of the user to read")):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})

    if user_data:
        user = User(**user_data)
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )


# Update User Endpoint
@app.put("/users/{user_id}", response_model=User)
async def update_user(updates: User,
    user_id: str = Path(..., title="The ID of the user to update")
    
):
    existing_user = users_collection.find_one({"_id": ObjectId(user_id)})

    if existing_user:
        # Update the existing user with the provided updates
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updates.dict()})
        
        # Fetch the updated user data
        updated_user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        updated_user = User(**updated_user_data)
        return updated_user
    else:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )

# Delete User Endpoint
@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: str = Path(..., title="The ID of the user to delete")):
    existing_user = users_collection.find_one({"_id": ObjectId(user_id)})

    if existing_user:
        # Delete the user and return the deleted user data
        users_collection.delete_one({"_id": ObjectId(user_id)})
        deleted_user = User(**existing_user)
        return deleted_user
    else:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )
        
