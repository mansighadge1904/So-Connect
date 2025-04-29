from django.db import models
from django.conf import settings
from django.db.models import Max
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user", null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="from_user", null=True)
    reciepient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_user", null=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    @staticmethod
    def send_message(from_user, to_user, body):
        sender_message = Message(
            user = from_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = False
        )
        sender_message.save()

        reciepient_message = Message(
            user = to_user,
            sender = from_user,
            reciepient = from_user,
            body = body,
            is_read = False
        )
        
        return sender_message
    
    # def get_message(user):
    #     users = []
    #     messages = Message.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by("-last")
    #     for message in messages:
    #         users.append({
    #             'user' : User.objects.get(pk=message['reciepient']),
    #             'last' : message['last'],
    #             'unread': Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False)
    #         })
    #     return users
    def get_message(user):
        users = []
        
        # Get messages where the logged-in user is either the sender or recipient
        messages = Message.objects.filter(
            models.Q(sender=user) | models.Q(reciepient=user)
        ).values('sender', 'reciepient').annotate(last=Max('date')).order_by("-last")
        
        for message in messages:
            # Check if the logged-in user is the sender or the recipient
            if message['sender'] != user.id:
                other_user = User.objects.get(pk=message['sender'])  # If the logged-in user is the recipient
            else:
                other_user = User.objects.get(pk=message['reciepient'])  # If the logged-in user is the sender
            
            users.append({
                'user': other_user,
                'last': message['last'],
                'unread': Message.objects.filter(user=user, reciepient__pk=other_user.id, is_read=False)
            })
        return users

