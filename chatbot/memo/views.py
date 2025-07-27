import time
import logging


from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer

from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .tasks import answer_user_request
from .utils import extract_post_request
from .brain import openai_chat_complete
from .vectorize import create_collection

logger = logging.getLogger(__name__)


class DocumentCreateView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


@csrf_exempt
@require_POST
def chat_complete(request):
    json_data = extract_post_request(request)
    bot_id = json_data.get("bot_id", "botOps")
    user_id = json_data.get("user_id")
    user_message = json_data.get("user_message")
    logger.info(f"Complete chat from user {user_id} to {bot_id}: {user_message}")
    task = answer_user_request.delay(bot_id, user_id, user_message)
    return JsonResponse({"task_id": task.id}, status=200)



@csrf_exempt
def get_chat_response(request, task_id):
    start_time = time.time()
    while True:
        task_result = AsyncResult(task_id)
        task_status = task_result.status
        logger.info(f"Task result: {task_result.result}")

        if task_status == 'PENDING':
            if time.time() - start_time > 60:  # 60 seconds timeout
                return {
                    "task_id": task_id,
                    "task_status": task_result.status,
                    "task_result": task_result.result,
                    "error_message": "Service timeout, retry please"
                }
            else:
                time.sleep(0.5)  # sleep for 0.5 seconds before retrying
        else:
            result = {
                "task_id": task_id,
                "task_status": task_result.status,
                "task_result": task_result.result
            }
            return JsonResponse(result, status=200)


@csrf_exempt
@require_POST
def create_vector_collection(request):
    json_data = extract_post_request(request)
    collection_name = json_data.get("collection_name")
    create_status = create_collection(collection_name)
    logging.info(f"Create collection {collection_name} status: {create_status}")
    return JsonResponse({"status": create_status is not None}, status=200)