from channels.routing import route, route_class
from otreechat.consumers import msg_consumer, ChatConsumer

# NOTE: otree_extensions is part of
# otree-core's private API, which may change at any time.
channel_routing = [
    route_class(ChatConsumer, path=r"^/otreechat/(?P<channel>[a-zA-Z0-9_-]+)/$"),
    route('otree.chat_messages', msg_consumer),
]
