import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from django.views import View
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.models import User  # Update if using a custom model
from django.views.generic.edit import CreateView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
class RegisterController(CreateView):

    def get(self, request):
        return render(request, 'admin/auth/register.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return JsonResponse({"status": "Failed", "message": "Passwords do not match!"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": 'Failed', "message": "Username is already taken"})

        if User.objects.filter(email=email).exists():
            return JsonResponse({"status": 'Failed', "message": "Email is already registered"})

        # Save user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        url = 'http://127.0.0.1:8000/login/'
        return JsonResponse({"status": "success", "message": "User registered successfully!", "redirect_url": url}, status=200)