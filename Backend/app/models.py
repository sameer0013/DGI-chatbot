from datetime import datetime

from django.db import models

from accounts.models import User


class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def response(self):
        return self.response_set.all()

class Response(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='response')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)