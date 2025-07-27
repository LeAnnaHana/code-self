from django.urls import path

from . import views

app_name = "memo"

urlpatterns = [
    path("complete", views.chat_complete, name="chat_complete"),
    path("complete/<str:task_id>", views.get_chat_response, name="get_chat_response"),
    path("collection/create", views.create_vector_collection, name="create_vector_collection"),
    path('documents/create/', views.DocumentCreateView.as_view(), name='document-create'),
]
