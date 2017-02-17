# In consumers.py
from channels import Group, Channel
from .models import ChatMessage, NicknameRegistration
from otree.models.participant import Participant
import json
from channels.generic.websockets import JsonWebsocketConsumer


def get_chat_group(channel):
    return 'otreechat-{}'.format(channel)


def msg_consumer(message):
    content = message.content

    # For now, don't create a model because we
    # don't yet have a way to export this table.
    # currently oTree admin is not extensible.

    channel = content['channel']
    channels_group = get_chat_group(channel)

    # list containing 1 element
    # it seems I can't use .get() because of idmap
    participant_id = Participant.objects.filter(code=content['participant_code']).values_list(
        'id', flat=True)[0]

    nickname = NicknameRegistration.objects.values_list(
        'nickname', flat=True).get(participant=participant_id, channel=channel)

    chat_message = {
        'channel': channel,
        'nickname': nickname,
        'body': content['body'],
        'participant_id': participant_id
    }

    Group(channels_group).send({'text': json.dumps([chat_message])})

    ChatMessage.objects.create(
        participant_id=participant_id,
        channel=channel,
        body=content['body'],
        nickname=nickname
    )


class ChatConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return [get_chat_group(kwargs['channel'])]

    def connect(self, message, **kwargs):
        history = ChatMessage.objects.filter(
            channel=kwargs['channel']).order_by('timestamp').values(
                'channel', 'nickname', 'body', 'participant_id'
        )

        # Convert ValuesQuerySet to list
        self.send(list(history))

    def receive(self, content, **kwargs):
        # Stick the message onto the processing queue
        Channel("otree.chat_messages").send(content)
