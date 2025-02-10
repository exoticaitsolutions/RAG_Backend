from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from RAG_CHATBOT_BACKEND_APIS import admin_view
from . import views
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.RegisterController import RegisterController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.LoginController import LoginController
# Define schema view for Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="File Upload API",
        default_version="v1",
        description="API for uploading PDFs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

# Grouped URL patterns
urlpatterns = [
  
]

# Admin Authentication
admin_auth_urls = [
    # Login Routes 
    path('login/', LoginController.as_view(), name='login.get'),
    # Register Routes
    path('register/', RegisterController.as_view(), name='register.get'),
]

# Admin Dashboard
admin_dashboard_urls = [
    path("dashboard/home/", admin_view.admin_dashborad_page, name="admin_dashborad_page"),
    path("dashboard/services/chatbot/create/", admin_view.admin_dashborad_add_assistant_page, name="admin_dashborad_add_assistant_page"),
    path("dashboard/services/chatbot/get/<str:c_id>/", admin_view.admin_dashborad_document_list, name="document-list"),
    path("dashboard/services/chatbot/preview/<str:c_id>/", admin_view.admin_dashboard_preview_chat_bot, name="preview-chatbot"),
    path("dashboard/services/chatbot/history/<str:c_id>/", admin_view.admin_dashborad_chatbot_history, name="chat-history"),
    path("dashboard/services/chatbot/setting/<str:c_id>/", admin_view.admin_dashborad_chatbot_setting, name="chat-setting"),
    path("dashboard/services/chatbot/chatbot-appearance/<str:c_id>/", admin_view.admin_dashborad_chatbot_setting_apperence, name="chat-setting-apperence"),
    path("dashboard/services/chatbot/delete/<str:c_id>/", admin_view.admin_dashborad_chatbot_delete, name="chat-setting-delete"),
    path("dashboard/services/chatbot/intergation/<str:c_id>/", admin_view.admin_dashborad_chatbot_share, name="chat-setting-intergation"),

    path('chatbot/', views.chatbot_view, name='chatbot'),


]

# Chatbot Services
chatbot_urls = [
   #  path("chatbot/chatbot-history/<str:c_id>/", admin_view.admin_dashborad_chatbot_history, name="chat-history"),
]

# API Endpoints
api_urls = [
    path("pdf/api/v1/upload-pdf/", views.upload_pdf_with_loader, name="upload_pdf_with_loader"),
    path("url/api/v1/upload-url/", views.upload_url_with_loader, name="upload_url_with_loader"),
    path("pdf/api/v1/query/", views.ChromaQueryAPIView, name="ChromaQueryAPIView"),
]

# Swagger Documentation
swagger_urls = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

# Combine all routes
urlpatterns += admin_auth_urls + admin_dashboard_urls + chatbot_urls + api_urls + swagger_urls

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
