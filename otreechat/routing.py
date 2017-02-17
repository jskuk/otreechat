from channels.routing import route, route_class
from otreechat.consumers import msg_consumer, ChatConsumer
from otree.channels.routing import channel_routing

channel_routing += [
    route_class(ChatConsumer, path=r"^/otreechat/(?P<room>[a-zA-Z0-9_-]+)/$"),
    route('otree.chat_messages', msg_consumer),
]
