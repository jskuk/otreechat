from django import template
register = template.Library()
import re

@register.inclusion_tag('otreechat/widget.html', takes_context=True)
def chat(context, *args, **kwargs):
    player = context['player']
    group = context['group']
    Constants = context['Constants']

    kwargs.setdefault('channel', group.id)
    kwargs.setdefault('nickname', 'Player {}'.format(player.id_in_group))

    # prefix the channel name with session code and app name
    context['channel'] = '{}-{}-{}'.format(
        context['session'].code,
        Constants.name_in_url,
        kwargs['channel']
    )

    context['nickname'] = kwargs['nickname']

    # channel name should not contain illegal chars,
    # so that it can be used in JS and URLs
    if not re.match(r'^[a-zA-Z0-9_-]+$', context['channel']):
        raise ValueError(
            "'channel' can only contain ASCII letters, numbers, underscores, and hyphens. "
            "Value given was: {}".format(context['channel']))

    return context