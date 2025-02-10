# Generated by Django 5.1.6 on 2025-02-07 11:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RAG_CHATBOT_BACKEND_APIS', '0014_alter_document_chatbot_alter_document_last_updated'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentCollectionIds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_id', models.CharField(default='', max_length=100)),
                ('doc_name', models.CharField(default='', max_length=500)),
                ('collection', models.CharField(default='', max_length=100)),
                ('chroma_dir', models.CharField(default='', max_length=100)),
                ('chatbot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RAG_CHATBOT_BACKEND_APIS.chatbotdb')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RAG_CHATBOT_BACKEND_APIS.document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
