from django.contrib.auth.models import User
from django.db import models

from item.models import Item

# Create your models here.

class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-modified_at',)

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)

    '''Conversation Model
Attributes:

item: A ForeignKey relationship to the Item model. This indicates that each conversation is related to a specific item, potentially for discussion or negotiation purposes. The related_name='conversations' allows access to a list of conversations from an Item instance.
members: A ManyToManyField relationship with the User model. This field defines the participants of the conversation. Through related_name='conversations', you can access a user's conversations.
created_at: A DateTimeField that automatically sets the timestamp when a new conversation is created (auto_now_add=True).
modified_at: Another DateTimeField similar to created_at but intended to track the last modification time. However, it seems there might be an oversight, as it's also set to auto_now_add=True, which means it will only set the timestamp upon creation and not update it on subsequent modifications.
Meta Options:

ordering: Specifies the default ordering of query results to be in descending order of modified_at. This means the most recently modified or created conversations will appear first.
ConversationMessage Model
Attributes:
conversation: A ForeignKey relationship to the Conversation model. This ties each message to a specific conversation.
content: A TextField to store the message's content.
created_at: A DateTimeField that records when the message was created, with auto_now_add=True to automatically set this when the message is saved.
created_by: A ForeignKey to the User model, indicating who created the message. The related_name='created_messages' allows accessing a list of messages created by a user.'''