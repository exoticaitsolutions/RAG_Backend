# Generated by Django 5.1.5 on 2025-02-03 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RAG_CHATBOT_BACKEND_APIS', '0003_fileupload_created_at_fileupload_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
