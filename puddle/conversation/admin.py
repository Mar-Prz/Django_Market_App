from django.contrib import admin

# Register your models here.

from .models import Conversation, ConversationMessage
#allows the models to be managed through the Django admin interface
admin.site.register(Conversation) 
admin.site.register(ConversationMessage)