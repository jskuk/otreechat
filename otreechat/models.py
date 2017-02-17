from django.db import models
from otree.models import Participant, Session


class ChatMessage(models.Model):
    participant = models.ForeignKey(Participant)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=255)
    message = models.TextField()
    nickname = models.CharField(max_length=255)
