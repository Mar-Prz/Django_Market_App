from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation
# Create your views here.

@login_required
def new_conversation(request, item_pk): #when you click contact seller you will be sent to this page
    item = get_object_or_404(Item, pk=item_pk) #get item from the database when the pk is item_pk

    if item.created_by == request.user: #if you are the owner you should not be able to visit this page
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id]) #get all of the conversations connected to this item where you are a member

    if conversations: #check if there already is a conversation with you and the owner
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method =='POST': #check if form has been submitted
        form = ConversationMessageForm(request.POST)

        if form.is_valid(): #if form is valid and the contact field is filled out correctly, then we can create the conversation
           conversation = Conversation.objects.create(item=item) 
           conversation.members.add(request.user) #add you to the conversation
           conversation.members.add(item.created_by) #add the owner to the conversation
           conversation.save()
            #now create the conversation message
           conversation_message = form.save(commit=False) #commit false so we dont get an error from the database
           conversation_message.conversation = conversation #reference to the conversation, so points up to it
           conversation_message.created_by = request.user #who created it
           conversation_message.save()

           return redirect('item:detail', pk=item_pk) #be redirected back to the item:detail where the pk=item_pk
    else:      
        form = ConversationMessageForm() #if it isn't a post request just create an empty form
#return and render the template
    return render(request, 'conversation/new.html', {
        'form': form
    })       

@login_required
def inbox(request):
     conversations = Conversation.objects.filter(members__in=[request.user.id]) #get all of the conversations connected to this item where you are a member

     return render(request, 'conversation/inbox.html', {
         'conversations': conversations
     })

@login_required
def detail(request, pk): #this pk is for the conversation and not the item
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk) #all the conversations you have

    if request.method =='POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    #render the conversation template
    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
