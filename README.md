# otree chat

Chat rooms for oTree so that participants can communicate with each other.

## Installation

```
pip install -U otreechat
```

In your project root, next to `settings.py`,
create a file `routing.py` containing this:

```python
from otree.channels.routing import channel_routing
import otreechat.routing
channel_routing += otreechat.routing.channel_routing
```

In settings.py:

-   Set `CHANNEL_ROUTING = 'routing.channel_routing'` 
    (this is the dotted path to your `channel_routing` variable in `routing.py`).
-   Add `'otreechat'` to `INSTALLED_APPS`, e.g. `INSTALLED_APPS = ['otree', 'otreechat']`  

Then run `otree resetdb`.

## Usage

Add this to the top of your template:

```
{% load otreechat %}
```
Then wherever you want a chatbox in the template, use:

```
{% chat %}
```

You can pass optional parameters `room` and/or `nickname` like this:

```
{% chat nickname=player.chat_nickname room=player.chat_room %}
```

-   `nickname` is the nickname that will be displayed for that user in the chat.
    If omitted, the nickname is `Player 1`, `Player 2`, etc. 
    (based on the player's `id_in_group`). 
    
-   `room` is the chat room's ID or "channel", meaning that if 2 players
    have the same `room`, they can chat with each other.
    `room` is not displayed in the user interface; it's just used internally.
    If omitted, the room is scoped to the group.
    
Here's an example implementation:    

```python
class Player(BasePlayer):

    def chat_nickname(self):
        return 'Villain {}'.format(self.id_in_group)

    def chat_room(self):
        '''
        Scope the room to the current session and current group,
        and then can further subdivide into odd/even players
        '''
        return '{}-{}-{}'.format(Constants.name_in_url, self.group.pk, self.id_in_group % 2)
```

### Styling

To customize the style, just include some CSS after the `{% chat %}` element,
e.g.:

```html
    {% chat %}

    <style>
        #otreechat .messages {
            height: 400px;
        }
        #otreechat .nickname {
            color: #0000FF;
            font-weight: bold;
        }
    </style>
```

