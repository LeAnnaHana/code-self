import json
import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Document
from .brain import get_embedding
from .vectorize import add_vector
from .configs import DEFAULT_COLLECTION_NAME
# Import chunk_text function if not already imported
from .utils import chunk_text
logger = logging.getLogger(__name__)

def add_doc_to_vector_db(instance):
    full_text = instance.title + ' ' + instance.content
    if not full_text:
        logger.error("Title and content is null") 
        return

    # Split text into chunks of 500 characters and add document title as tag
    if len(full_text) > 500:
        chunks = chunk_text(full_text, 500)
        # Add document title as tag to each chunk
        chunks = [f"{instance.title}: {chunk}" for chunk in chunks]
    else:
        chunks = [f"{instance.title}: {full_text}"]
    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk)
        logger.info(f"Embedding {chunk} to vector")
        vector_id = instance.id * 100 + i
        add_vector(
            DEFAULT_COLLECTION_NAME,
            {
                vector_id: {
                    "vector": vector,
                    "payload": {
                        "title": instance.title,
                        "content": chunk,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                }
            }
        )


@receiver(post_save, sender=Document)
def create_document_to_vector_db(sender, instance, created, **kwargs):
    logger.info("create_document_to_vector_db")
    if created:
        add_doc_to_vector_db(instance)


@receiver(post_save, sender=Document)
def update_document_to_vector_db(sender, instance, **kwargs):
    logger.info("update_document_to_vector_db")
    add_doc_to_vector_db(instance)
