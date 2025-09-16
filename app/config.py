import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG if needed
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("multi-agent-api")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "multi_agent_db")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

# Collections
context_collection = mongo_db["contexts"]
metadata_collection = mongo_db["metadata"]