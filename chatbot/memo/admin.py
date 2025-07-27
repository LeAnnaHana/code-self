from django.contrib import admin
from .models import Document, Nodes, ChatConversation

admin.site.register(Document)
admin.site.register(Nodes)
admin.site.register(ChatConversation)