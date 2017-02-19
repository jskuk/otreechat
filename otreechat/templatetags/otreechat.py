from django import template
register = template.Library()
import re
from otreechat.models import NicknameRegistration
from otree.api import safe_json

@register.inclusion_tag('otreechat/widget.html', takes_context=True)
def chat(context, *args, **kwargs):
    player = context['player']
    group = context['group']
    Constants = context['Constants']
    participant = context['participant']

    kwargs.setdefault('channel', group.id)
    kwargs.setdefault('nickname', 'Player {}'.format(player.id_in_group))

    # prefix the channel name with session code and app name
    channel = '{}-{}-{}'.format(
        context['session'].id,
        Constants.name_in_url,
        kwargs['channel']
    )

    nickname = kwargs['nickname']

    # channel name should not contain illegal chars,
    # so that it can be used in JS and URLs
    if not re.match(r'^[a-zA-Z0-9_-]+$', channel):
        raise ValueError(
            "'channel' can only contain ASCII letters, numbers, underscores, and hyphens. "
            "Value given was: {}".format(context['channel']))

    NicknameRegistration.objects.update_or_create(
        participant=participant,
        channel=channel,
        defaults={'nickname': nickname}
    )

    context['channel'] = channel

    vars_for_js = {
        'channel': context['channel'],
        'participant_code': participant.code,
        'participant_id': participant.id
    }

    context['vars_for_js'] = safe_json(vars_for_js)

    return context
