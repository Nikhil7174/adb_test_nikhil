"""
Separate Data Access Layer (Repository Pattern):

Create an abstract repository interface to adhere to DIP.

Implement a MongoDB repository for concrete data operations.
"""
from abc import ABC, abstractmethod
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging

logger = logging.getLogger(__name__)

class BaseTodoRepository(ABC):
    @abstractmethod
    def get_all_todos(self):
        pass

    @abstractmethod
    def create_todo(self, description: str):
        pass

class MongoTodoRepository(BaseTodoRepository):
    def __init__(self, client: MongoClient, database_name: str, collection_name: str):
        self.collection = client[database_name][collection_name]

    def get_all_todos(self):
        try:
            todos = list(self.collection.find({}))
            return [
                {"id": str(todo["_id"]), "description": todo["description"]}
                for todo in todos
            ]
        except PyMongoError as e:
            logger.error(f"MongoDB query failed: {e}")
            raise DatabaseError("Failed to fetch TODOs") from e

    def create_todo(self, description: str):
        try:
            result = self.collection.insert_one({"description": description})
            return {"id": str(result.inserted_id), "description": description}
        except PyMongoError as e:
            logger.error(f"MongoDB insert failed: {e}")
            raise DatabaseError("Failed to create TODO") from e

class DatabaseError(Exception):
    pass