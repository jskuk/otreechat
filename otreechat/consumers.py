# In consumers.py
from channels import Group, Channel
from .models import ChatMessage
from otree.models import Participant
import json

def get_chat_group(room):
    return 'otreechat-{}'.format(room)

from channels.generic.websockets import JsonWebsocketConsumer

def msg_consumer(message):
    content = message.content

    ChatMessage.objects.create(
        participant=Participant.objects.get(code=content['participant_code']),
        room=content['room'],
        message=content['message'],
        nickname=content['nickname']
    )

    room = content['room']
    grp = get_chat_group(room)
    Group(grp).send({'text': json.dumps(content)})


class ChatConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return [get_chat_group(kwargs['room'])]

    def receive(self, content, **kwargs):
        # Stick the message onto the processing queue
        Channel("otree.chat_messages").send(content)
