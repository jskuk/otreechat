from django import template
register = template.Library()
import re

@register.inclusion_tag('otreechat/room.html', takes_context=True)
def chat(context, *args, **kwargs):
    player = context['player']
    group = context['group']
    Constants = context['Constants']

    context.update({
        'room': '{}-{}'.format(Constants.name_in_url, group.id),
        'nickname': 'Player {}'.format(player.id_in_group),
    })

    # can override room and nickname
    context.update(kwargs)

    # room name should not contain illegal chars,
    # so that it can be used in JS and URLs

    if not re.match(r'^[a-zA-Z0-9_-]+$', context['room']):
        raise ValueError(
            "'room' can only contain ASCII letters, numbers, underscores, and hyphens. "
            "Value given was: {}".format(context['room']))

    return context