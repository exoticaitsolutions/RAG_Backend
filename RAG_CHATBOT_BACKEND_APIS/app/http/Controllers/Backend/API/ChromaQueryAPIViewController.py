import logging
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from RAG_CHATBOT_BACKEND_APIS.app.services.ChatGptQuery.ChatGPTQueryServices import GetResponseFromQuery
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# Configure Logger
logger = logging.getLogger(__name__)


class ChromaQueryAPIViewController(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]


    # Define Swagger request parameters correctly for form-data requests
    @swagger_auto_schema(
        operation_description="Query the ChromaDB for chatbot responses.",
        manual_parameters=[
            openapi.Parameter(
                "query", openapi.IN_FORM, description="The user's input query.", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                "chat_id", openapi.IN_QUERY, description="Chatbot ID", type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                "user_id", openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER, required=True
            ),
        ],
        responses={
            200: openapi.Response(
                "Successful response",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"results": openapi.Schema(type=openapi.TYPE_STRING, description="Chatbot response")},
                ),
            ),
            400: openapi.Response("Bad Request: Missing or invalid parameters"),
            404: openapi.Response("Not Found: Invalid chatbot or user ID"),
            500: openapi.Response("Internal Server Error"),
        },
    )
    def post(self, request, *args, **kwargs):
        """Handles chatbot queries using ChromaDB and returns AI-generated responses."""
        query = request.data.get('query')
        chat_id = request.GET.get("chat_id")
        user_id = request.GET.get("user_id")

        if not chat_id or not user_id:
            logger.error("Missing chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Missing chat_id or user_id"}, status=400)
        if not query:
            return JsonResponse({"error": "Query parameter is missing"}, status=400)

        try:
            chat_id = int(chat_id)
            user_id = int(user_id)
        except ValueError:
            logger.error("Invalid format for chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Invalid chat_id or user_id format"}, status=400)

        # Validate chatbot existence
        chatbot = ChatBotDB.objects.filter(id=chat_id, user_id=user_id).first()
        if not chatbot:
            logger.error(f"Chatbot with id {chat_id} not found for user {user_id}")
            return JsonResponse({"status": "failed", "message": "Invalid chat_id"}, status=404)

        # Validate user existence
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error(f"User with id {user_id} not found")
            return JsonResponse({"status": "failed", "message": "Invalid user_id"}, status=404)

        # Process query using ChatGPT
        try:
            results = GetResponseFromQuery(chatbot, user, query)
            return JsonResponse({"results": results}, safe=False, status=200)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)
