import motor.motor_asyncio
import os

MONGO_Details = os.getenv("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_Details)
database = client.Blog
userCollection = database.get_collection("Users")
blogCollection = database.get_collection("Blogs")