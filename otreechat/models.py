from django.db import models
from otree.models import Participant
import time

class ChatMessage(models.Model):
    class Meta:
        index_together = ['channel', 'timestamp']

    # the name "channel" here is unrelated to Django channels
    channel = models.CharField(max_length=255)
    participant = models.ForeignKey(Participant)
    nickname = models.CharField(max_length=255)

    # call it 'body' instead of 'message' or 'content' because those terms
    # are already used by channels
    body = models.TextField()
    timestamp = models.FloatField(default=time.time)


class NicknameRegistration(models.Model):
    '''For security, have to register the nicknames on the server side'''

    class Meta:
        unique_together = ['channel', 'participant']

    channel = models.CharField(max_length=255)
    participant = models.ForeignKey(Participant)
    nickname = models.CharField(max_length=255)