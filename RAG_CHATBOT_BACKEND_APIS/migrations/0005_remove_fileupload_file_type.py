# Generated by Django 5.1.5 on 2025-02-03 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RAG_CHATBOT_BACKEND_APIS', '0004_alter_fileupload_file_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileupload',
            name='file_type',
        ),
    ]
