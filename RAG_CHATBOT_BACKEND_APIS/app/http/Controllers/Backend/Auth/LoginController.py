import re
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout, authenticate, login
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User  # Update if using a custom model
# Set up logging
logger = logging.getLogger(__name__)

class LoginController(View):

    def get(self, request):
        return render(request, 'admin/auth/login.html')

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        username_or_address = request.POST.get('username_or_address')
        print('username_or_address', username_or_address)
        password = request.POST.get('password')
        print('password',password )
        if not username_or_address or not password:
            logger.warning("Login attempt with missing credentials")
            return JsonResponse({"status": "failed", "message": "Username and password are required."}, status=400)

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, username_or_address):
            try:
                user = User.objects.get(email=username_or_address)  # Try to authenticate by email
            except User.DoesNotExist:
                user = None 
        else:
            logger.info(f"Attempting login with username: {username_or_address}")
            try:
                user = User.objects.get(username=username_or_address)  # Try to authenticate by email
            except User.DoesNotExist:
                user = None 
        logger.info(f"User {user} logged in successfully")
        if user is not None:
            if user and user.check_password(password):  # Check the password
                login(request, user)
                url = 'http://127.0.0.1:8000/dashboard/home/'
                return JsonResponse({"status": "success", "message": "User logged in successfully!", "redirect_url": url}, status=200)
            else:
                return JsonResponse({"status": "failed", "message": "Invalid username or password!"})
        else:
            logger.warning(f"Failed login attempt for: {username_or_address}")
            return JsonResponse({"status": "failed", "message": "Invalid username or password!"})
