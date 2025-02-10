import os
from django.db import models
from django.contrib.auth.models import User  # Update if using a custom model


class ChatbotAppearance(models.Model):
    chatbot_id = models.CharField(max_length=50)
    display_name = models.TextField(max_length=2000)
    footer_name = models.TextField(max_length=2000, default="Powered by My AI Solutions.")
    # chatbot_title = models.CharField(max_length=255, default="Welcome")
    initial_message = models.TextField(blank=True, default="Hi! What can I help with you?")
    chatbot_theme = models.CharField(max_length=10, default="#8d54a2", blank=True)
    chatbot_mode = models.BooleanField(default=False)
    suggested_messages = models.TextField(blank=True)
    chatbot_image = models.ImageField(upload_to='chatbot_images/', default=r"default_images/chatbot_image.png",
                                      null=True, blank=True)
    chatbot_launcher_icon = models.ImageField(upload_to='launcher_icon/', default=r"default_images/avatar-1.png",
                                              null=True, blank=True)
    top_bar_background = models.CharField(max_length=10, default="#8d54a2")
    top_bar_textcolor = models.CharField(max_length=10, default="#000000")
    bot_message_background = models.CharField(max_length=10, default="#ffffff")
    bot_message_color = models.CharField(max_length=10, default="#46464e")
    user_message_background = models.CharField(max_length=10, default="#ffffff")
    user_message_color = models.CharField(max_length=10, default="#46464e")
    chatbot_background_color = models.CharField(max_length=10, default="#e6e6e6")
    chatbot_background_pattern = models.ImageField(upload_to='chatbot_background_patterns/', blank=True)
    font_family = models.CharField(max_length=255, default="Arial")
    font_size = models.PositiveIntegerField(blank=True, default=14)
    widget_width = models.PositiveIntegerField(blank=True, default=25)
    widget_height = models.PositiveIntegerField(blank=True, default=450)
    widget_position = models.CharField(max_length=5, default="right")  # Assumes 'right' or 'left, blank=True'
    show_popup_notification = models.BooleanField(default=True)
    delay_showing_popup_notification = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
# CHat bot db 
PINECONE_INDEX_NAME = str(os.getenv("PINECONE_INDEX_NAME"))
class ChatBotDB(models.Model):
    STATUS_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('restricted', 'Restricted'),
    )
    LOGIN_STATUS = (
        ("anonymous", 'Anonymous'),
        ("login", 'Login')
    )
    LLM_MODEL = (
        ("system openai", 'System OpenAi'),
        ("private openai", 'Private OpenAi'),
        ("gpt4all", 'GPT4ALL'),
        ("huggingface", 'HuggingFace'),
    )
    MODEL = (
        ("gpt-3.5-turbo", 'gpt-3.5-turbo'),
        ("gpt-4", 'gpt-4'),
    )
    VECTOR_DATABASE = (
        ("chroma", 'Chroma'),
        ("pinecone", 'Pinecone'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # visitor = models.ForeignKey('VisitorVisits', on_delete=models.CASCADE)
    chatbot_name = models.CharField(max_length=200)
    llm_model = models.CharField(choices=LLM_MODEL, default="system openai", max_length=50)
    model = models.CharField(choices=MODEL, default="gpt-3.5-turbo", max_length=50)
    openai_key = models.TextField(default="")
    vector_database = models.CharField(choices=VECTOR_DATABASE, default="chroma", max_length=200)
    pinecone_key = models.CharField(default="", max_length=200)
    pinecone_env = models.TextField(default="")
    pinecone_user_index = models.CharField(default="", max_length=200)
    temperature = models.FloatField(default=0.4)
    context = models.TextField(
        default="""You are a conversational chatbot and Use the following pieces of context to answer the question at the end. You will try your best to give a logical answer. If you don't know the answer, just say that you don't know, don't try to make up an answer""")
    # random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    chatbot_id = models.CharField(max_length=50)
    hits = models.PositiveIntegerField(default=10)
    seconds = models.PositiveIntegerField(default=60)
    visibility = models.CharField(max_length=50, default='private')
    login_status = models.CharField(max_length=20, choices=LOGIN_STATUS, default='login')
    icon_url = models.ImageField(upload_to='chatbot', default=r"/media/default_images/chatbot_image.png")
    chatbot_appearance = models.ForeignKey("ChatbotAppearance", on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Document Database 
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE, blank=True)
    def upload_path(instance, filename): # type: ignore
        # Ensure filename is safe
        filename = os.path.basename(filename)
        return f'uploads/{instance.user.username}/{instance.chatbot.chatbot_name}/{filename}'
    filepath = models.FileField(upload_to=upload_path)
    name = models.CharField(default="", max_length=250)
    size = models.CharField(default="", max_length=250)
    no_of_characters = models.PositiveIntegerField(default=0, blank=True)
    no_of_chunks = models.PositiveIntegerField(default=0, blank=True)
    status = models.CharField(default="pending", max_length=10)
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.name

class DocumentNamespaceIds(models.Model):
    doc_id = models.CharField(default="", max_length=100)
    doc_name = models.CharField(default="", max_length=500)
    namespace = models.CharField(default="", max_length=100)
    index_name = models.CharField(default=PINECONE_INDEX_NAME, max_length=100)
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey("Document", on_delete=models.CASCADE)  


class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)  # Updated timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Updated timestamp
    pdf_embedding_status = models.CharField(max_length=20, default="pending")
    pdf_embadding_error_or_message = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"File: {self.file.name}, Uploaded: {self.uploaded_at}"

class DocumentCollectionIds(models.Model):
    doc_id = models.CharField(default="", max_length=100)
    doc_name = models.CharField(default="", max_length=500)
    collection = models.CharField(default="", max_length=100)
    chroma_dir = models.CharField(default="", max_length=100)
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey("Document", on_delete=models.CASCADE)