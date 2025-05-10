from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import ChatMessage, ChatGroup, GroupMessage
from social.models import Follow  # assuming you have a Follow model to track follows

User = get_user_model()

@login_required
def chitchat_view(request, username=None):
    # Get users the logged-in user is following
    followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    followed_users_list = User.objects.filter(id__in=followed_users)

    # Get users who have sent messages to the logged-in user
    sent_messages_users = ChatMessage.objects.filter(receiver=request.user).values('sender').distinct()
    users_sent_messages = User.objects.filter(id__in=[user['sender'] for user in sent_messages_users])

    # Combine followed users and users who sent messages, but avoid duplicates
    users_in_chat = followed_users_list | users_sent_messages

    selected_user = None
    messages = []

    if username:
        selected_user = get_object_or_404(User, username=username)
        # Get chat messages between the two users
        messages = ChatMessage.objects.filter(
            sender__in=[request.user, selected_user],
            receiver__in=[request.user, selected_user]
        ).order_by('timestamp')

    groups = ChatGroup.objects.filter(members=request.user)

    context = {
        'users': users_in_chat,
        'selected_user': selected_user,
        'messages': messages,
        'groups': groups,
    }
    return render(request, 'chitchat.html', context)



@login_required
def send_message(request):
    if request.method == 'POST':
        if 'receiver' in request.POST:  # Private message
            receiver_username = request.POST['receiver']
            receiver = User.objects.get(username=receiver_username)
            message_content = request.POST['message']
            # Check if the message content is not empty
            if message_content.strip():
                message = ChatMessage(sender=request.user, receiver=receiver, message=message_content)
                message.save()
        elif 'group_id' in request.POST:  # Group message
            group_id = request.POST['group_id']
            group = ChatGroup.objects.get(id=group_id)
            message_content = request.POST['content']
            # Check if the message content is not empty
            if message_content.strip():
                message = GroupMessage(group=group, sender=request.user, message=message_content)
                message.save()

        return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page
    else:
        return HttpResponse("Invalid request", status=400)

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        members = request.POST.getlist('members')  # list of usernames

        if group_name and members:
            group = ChatGroup.objects.create(name=group_name, creator=request.user)
            group.members.set(User.objects.filter(username__in=members))
            group.members.add(request.user)  # add creator
            return redirect('chat_group', group_id=group.id)

    users = User.objects.exclude(username=request.user.username)
    return render(request, 'create_group.html', {'users': users})

@login_required
def chat_group_view(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)

    # Check if the logged-in user is a member of the group
    if request.user not in group.members.all():
        return redirect('chitchat')  # or return an error message

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            GroupMessage.objects.create(
                group=group,
                sender=request.user,
                message=message
            )
            return redirect('chat_group', group_id=group.id)

    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')
    return render(request, 'chitchat.html', {
        'group': group,
        'selected_group': group,
        'messages': messages,
        'users': User.objects.exclude(id=request.user.id),
        'groups': ChatGroup.objects.filter(members=request.user),
    })