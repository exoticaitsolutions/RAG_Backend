# Generated by Django 5.1.5 on 2025-02-03 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RAG_CHATBOT_BACKEND_APIS', '0005_remove_fileupload_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='pdf_embadding_error_or_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileupload',
            name='pdf_embadding_status',
            field=models.BooleanField(default=False),
        ),
    ]
