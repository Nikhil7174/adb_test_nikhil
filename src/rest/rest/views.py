"""
Centralized Error Handling:

Use a decorator to handle database exceptions and reduce code duplication.

Dependency Injection:

Inject the repository dependency into the view to decouple it from specific implementations.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from pymongo import MongoClient
from .todo_repositories import MongoTodoRepository, DatabaseError
from .serializers import TodoSerializer
import functools
import logging

logger = logging.getLogger(__name__)

def handle_db_errors(view_method):
    @functools.wraps(view_method)
    def wrapper(self, request, *args, **kwargs):
        try:
            return view_method(self, request, *args, **kwargs)
        except DatabaseError:
            logger.error("Database operation failed")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper

class TodoListView(APIView):
    def __init__(self):
        client = MongoClient(self._get_mongo_uri())
        self.repository = MongoTodoRepository(
            client=client,
            database_name=settings.MONGO_CONFIG['DATABASE'],
            collection_name=settings.MONGO_CONFIG['COLLECTION']
        )

    def _get_mongo_uri(self):
        config = settings.MONGO_CONFIG
        return f"mongodb://{config['HOST']}:{config['PORT']}/"

    @handle_db_errors
    def get(self, request):
        todos = self.repository.get_all_todos()
        return Response({"todos": todos}, status=status.HTTP_200_OK)

    @handle_db_errors
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = self.repository.create_todo(serializer.validated_data['description'])
        return Response(todo, status=status.HTTP_201_CREATED)