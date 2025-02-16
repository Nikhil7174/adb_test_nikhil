from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, logging, os
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import PyMongoError

MONGO_HOST = os.environ.get("MONGO_HOST", "mongo")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)

mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
db = MongoClient(mongo_uri)['test_db']
logger = logging.getLogger(__name__)

class TodoListView(APIView):
    def get(self, request):
        """
        Fetch all TODOs from MongoDB.
        Returns: List of TODOs with id and description.
        """
        try:
            todos = list(db.todos.find({}))
            
            # Convert MongoDB ObjectId to string for JSON serialization
            formatted_todos = [
                {"id": str(todo["_id"]), "description": todo["description"]}
                for todo in todos
            ]
            
            return Response({"todos": formatted_todos}, status=status.HTTP_200_OK)
            
        except PyMongoError as e:
            logger.error(f"MongoDB query failed: {str(e)}")
            return Response(
                {"error": "Failed to fetch TODOs"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        Create a new TODO in MongoDB.
        Expects: { "description": "string" }
        Returns: Created TODO with ID.
        """
        try:
            description = request.data.get("description")
            
            # Input validation
            if not description or not description.strip():
                return Response(
                    {"error": "Description cannot be empty"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            result = db.todos.insert_one({"description": description.strip()})
            
            return Response(
                {"id": str(result.inserted_id), "description": description},
                status=status.HTTP_201_CREATED
            )
            
        except PyMongoError as e:
            logger.error(f"MongoDB insert failed: {str(e)}")
            return Response(
                {"error": "Failed to create TODO"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )