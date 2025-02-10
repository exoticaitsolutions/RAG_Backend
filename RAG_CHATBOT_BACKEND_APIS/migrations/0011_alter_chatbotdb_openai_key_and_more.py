# Generated by Django 5.1.6 on 2025-02-07 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RAG_CHATBOT_BACKEND_APIS', '0010_chatbotappearance_remove_fileupload_thread_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbotdb',
            name='openai_key',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='chatbotdb',
            name='pinecone_env',
            field=models.TextField(default=''),
        ),
    ]
