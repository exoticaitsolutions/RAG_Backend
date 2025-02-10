from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt


class DocumentController:
    def show_upload_form(self, request, c_id):
        """ Renders the document upload form """
        return render(request, 'admin/page/chatbot/pages/add-doucument-list.html')
    
    def upload_and_train(self, request,c_id):
        
        return JsonResponse({
                "message": "Document uploaded and trained successfully",
        "training_result": 'training_result'
    })

    


