from pymongo import MongoClient
import redis
import os

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(mongo_uri)
db = client["Library"]

stores_collection = db["Stores"]
books_collection = db["Books"]


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)

redis_client = redis.StrictRedis(host=redis_host, port=int(redis_port), decode_responses=True)