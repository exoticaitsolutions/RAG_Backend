# Generated by Django 5.1.6 on 2025-02-07 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RAG_CHATBOT_BACKEND_APIS', '0012_documentnamespaceids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='chatbot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RAG_CHATBOT_BACKEND_APIS.chatbotdb'),
        ),
        migrations.AlterField(
            model_name='document',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
