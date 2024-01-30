import motor.motor_asyncio

MONGO_Details = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_Details)
database = client.Blog
userCollection = database.get_collection("Users")
blogCollection = database.get_collection("Blogs")