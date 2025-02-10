from django.shortcuts import redirect
from django.urls import resolve

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract the resolved URL name
        resolved_url = resolve(request.path_info).url_name
        # List of protected admin routes
        protected_routes = [
            "admin_dashborad_page",
            "admin_dashborad_add_assistant_page",
            "document-list",
            "preview-chatbot",
            "chat-history",
            "chat-setting",
            "chat-setting-apperence",
            "chat-setting-delete",
            "chat-setting-intergation",
        ]

        # If user is not authenticated and accessing a protected route, redirect to login
        if not request.user.is_authenticated and resolved_url in protected_routes:
            return redirect('/login/')  # Redirect to the login page

        return self.get_response(request)
