from django.db import models

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)  # Updated timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Updated timestamp
    pdf_embedding_status = models.CharField(max_length=20, default="pending")
    pdf_embadding_error_or_message = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"File: {self.file.name}, Uploaded: {self.uploaded_at}"

class UrlUpload(models.Model):
    url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url_embedding_status = models.CharField(max_length=50, default='pending')
    url_embedding_error_or_message = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"URL Upload {self.url}"