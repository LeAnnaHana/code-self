from django.apps import AppConfig
from django.db.models.signals import post_save


class MemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'memo'

    def ready(self):
        from .models import Document
        from .signals import create_document_to_vector_db, update_document_to_vector_db
        post_save.connect(create_document_to_vector_db, sender=Document)
        post_save.connect(update_document_to_vector_db, sender=Document)
