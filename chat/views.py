from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q, Max
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def inbox(request):
    user = request.user
    # Get all users who have sent messages to this user (or vice versa)
    messages = Message.get_message(user=user)
    
    active_direct = None
    directs = None

    if messages:
        # Get the first message to set as the active chat
        first_message = messages[0]
        active_direct = first_message['user'].username
        
        # Get all messages between the logged-in user and the active recipient (sender/receiver)
        directs = Message.objects.filter(
            (Q(sender=user) & Q(reciepient=first_message['user'])) |
            (Q(sender=first_message['user']) & Q(reciepient=user))
        ).order_by('date')  # Ensure the order of messages
        
        # Mark all the messages as read for the active chat
        directs.update(is_read=True)

        # Update the unread count for each user in the inbox (this part can be customized)
        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0  # Update unread count to 0 if the chat is active
        
        if request.method == "POST":
            body = request.POST.get('body')
            if body:
                sender = user
                to_user_username = request.POST.get('to_user')
                if body and to_user_username:
                    sender = user
                    try:
                        recipient = User.objects.get(username=to_user_username)
                        Message.send_message(sender, recipient, body)
                    except Message.DoesNotExist:
                        pass
                    return redirect('inbox')

        # Prepare context with the necessary data
        context = {
            'directs': directs,
            'active_direct': active_direct,
            'messages': messages,  # Send the unique messages list here
            'users': User.objects.exclude(username=user.username)  # Exclude the logged-in user from the list
        }

        return render(request, 'inbox.html', context)

    # If no messages exist
    context = {'directs': [], 'active_direct': None, 'messages': []}
    return render(request, 'inbox.html', context)




def chat_sidebar(request):
    # Get the messages for the logged-in user from the 'get_message' method
    messages = Message.get_message(request.user)

    # Prepare the context
    context = {
        'messages': messages,
    }

    return render(request, 'chat/chat_sidebar.html', context)

def get_message(user):
    # Get the messages where the logged-in user is either the sender or the recipient
    messages = Message.objects.filter(
        Q(sender=user) | Q(reciepient=user)
    ).values('sender', 'reciepient').annotate(last=Max('date')).order_by("-last")
    
    # Create a set to track unique users
    seen_users = set()
    unique_users = []

    for message in messages:
        # Determine the user involved (sender or recipient)
        if message['sender'] != user.id:
            other_user = User.objects.get(pk=message['sender'])  # If the logged-in user is the recipient
        else:
            other_user = User.objects.get(pk=message['reciepient'])  # If the logged-in user is the sender

        # Only add the user if they haven't been added yet
        if other_user.id not in seen_users:
            seen_users.add(other_user.id)
            unique_users.append({
                'user': other_user,
                'last': message['last'],
                'unread': Message.objects.filter(user=user, reciepient__pk=other_user.id, is_read=False).count()
            })

    return unique_users

