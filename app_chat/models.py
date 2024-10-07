from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    to_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='recieved_messages')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:50]
