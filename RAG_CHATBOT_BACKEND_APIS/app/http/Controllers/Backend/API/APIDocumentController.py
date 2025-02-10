import logging
import os
import threading
import socket
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from RAG_CHATBOT_BACKEND_APIS.app.http.Serializers.DocumentUpload import DocumentUploadSerializer
from RAG_CHATBOT_BACKEND_APIS.app.services.training.train_document import uploaded_document_and_train_llm
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, DocumentNamespaceIds

# Configure Logger
logger = logging.getLogger(__name__)

class APIDocumentController(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Correct placement of parser_classes

    @swagger_auto_schema(
        operation_description="Upload PDF documents and trigger LLM training.",
        manual_parameters=[
            openapi.Parameter("chat_id", openapi.IN_QUERY, description="Chatbot ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter("user_id", openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter("file1", openapi.IN_QUERY, description="file1 ID", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            201: openapi.Response("Success", openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="Status of the request"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                "uploaded_files": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
            })),
            400: openapi.Response("Bad Request: Missing or invalid parameters"),
            404: openapi.Response("Not Found: Invalid chatbot or user ID"),
            500: openapi.Response("Internal Server Error"),
        },
    )
    def post(self, request, *args, **kwargs):
        """Handles PDF document uploads and triggers LLM training."""
        logger.info("Received document upload request")

        # Get `chat_id` and `user_id` from the request
        chat_id = request.GET.get("chat_id")
        user_id = request.GET.get("user_id")

        if not chat_id or not user_id:
            logger.error("Missing chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Missing chat_id or user_id"}, status=400)

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
        user = User.objects.filter(id=user_id).first()
        if not user:
            logger.error(f"User with id {user_id} not found")
            return JsonResponse({"status": "failed", "message": "Invalid user_id"}, status=404)

        # Check if files were uploaded
        if not request.FILES:
            logger.error("No files uploaded")
            return JsonResponse({"status": "failed", "message": "No files uploaded"}, status=400)

        uploaded_documents = []

        try:
            for file_key in request.FILES:
                uploaded_file = request.FILES[file_key]
                file_name = uploaded_file.name

                logger.info(f"Processing file: {file_name}")

                # Define file storage path
                user_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', user.username, chatbot.chatbot_name)
                os.makedirs(user_dir, exist_ok=True)  # Ensure directory exists

                media_file = os.path.join(user_dir, file_name)
                
                # Remove existing file
                if os.path.isfile(media_file):
                    logger.warning(f"Existing file found, removing: {media_file}")
                    os.remove(media_file)

                # Check if document already exists in database
                if DocumentNamespaceIds.objects.filter(doc_name=media_file).exists():
                    logger.info(f"Document {file_name} already exists in namespace")

                # Save file to media storage
                saved_path = default_storage.save(media_file, uploaded_file)

                # Prepare serializer data
                data = {
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "filepath": saved_path,
                    "name": uploaded_file.name,
                    "size": uploaded_file.size
                }

                serializer = DocumentUploadSerializer(data=data)
                if serializer.is_valid():
                    document_instance = serializer.save()
                    uploaded_documents.append(serializer.data)
                    logger.info(f"Document {file_name} uploaded successfully")

                    # Start document processing in a separate thread
                    try:
                        threading.Thread(target=uploaded_document_and_train_llm, args=(serializer.data, saved_path, chatbot, user)).start()
                        logger.info(f"Started LLM training thread for: {file_name}")
                    except Exception as e:
                        logger.error(f"Failed to start thread for document {file_name}: {str(e)}")
                        document_instance.status = "error"
                        document_instance.save()

                else:
                    logger.error(f"Document upload failed: {serializer.errors}")
                    return JsonResponse({"status": "failed", "errors": serializer.errors}, status=400)

            return JsonResponse({
                "status": "success",
                "message": "Documents uploaded and saved successfully",
                "uploaded_files": uploaded_documents
            }, status=201)

        except socket.error as e:
            logger.error(f"Socket error encountered: {str(e)}")
            return JsonResponse({"status": "failed", "message": "Network error occurred"}, status=500)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"status": "failed", "message": "An unexpected error occurred"}, status=500)
