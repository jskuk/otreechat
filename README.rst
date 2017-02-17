oTree Chat (beta)
=================

Chat rooms for oTree so that participants can communicate with each other.

This is an early beta version and subject to changes/improvements!

Installation
------------

(Assuming you already have an oTree project.)

.. code-block::

    pip install -U otreechat

In your project root, next to ``settings.py``,
create a file ``routing.py`` containing this:

.. code-block:: python

    from otree.channels.routing import channel_routing
    import otreechat.routing
    channel_routing += otreechat.routing.channel_routing

In ``settings.py``:

-   Set ``CHANNEL_ROUTING = 'routing.channel_routing'`` 
    (this is the dotted path to your ``channel_routing`` variable in ``routing.py``).
-   Add ``'otreechat'`` to ``INSTALLED_APPS``, e.g. ``INSTALLED_APPS = ['otree', 'otreechat']``  

Then run ``otree resetdb``.

Usage
-----

Basic usage
~~~~~~~~~~~

Add this to the top of your template:

.. code-block:: html+django

    {% load otreechat %}

Then wherever you want a chatbox in the template, use:

.. code-block:: html+django

    {% chat %}

This will make a chat room among players in the same Group,
where each player's nickname is displayed as
"Player 1", "Player 2", etc. (based on the player's ``id_in_group``).

Customizing the nickname and chat room members
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can pass optional parameters ``channel`` and/or ``nickname`` like this:

.. code-block:: html+django

    {% chat nickname=mynickname channel=mychannel %}

-   ``nickname`` is the nickname that will be displayed for that user in the chat.
    A typical usage would be ``{% chat nickname=player.role %}``.

-   ``channel`` is the chat room's ID, meaning that if 2 players
    have the same ``channel``, they can chat with each other.
    ``channel`` is not displayed in the user interface; it's just used internally.
    Its default value is ``group.id``, meaning all players in the group can chat together.
    You can use ``channel`` to instead scope the chat to the current page
    or sub-division of a group, etc. (see examples below).
    Regardless of the value of the ``channel`` argument,
    the chat will at least be scoped to players in the same session and the same app.

Here's an example where instead of communication within a group,
we have communication between groups based on role,
e.g. all buyers can talk with each other,
and all sellers can talk with each other.


.. code-block:: python

    class Player(BasePlayer):

        def role(self):
            if self.id_in_group == 1:
                return 'Seller'
            else:
                return 'Buyer'

Then in the template:

.. code-block:: html+django

    {% chat nickname=player.role channel=player.role %}

Styling
~~~~~~~

To customize the style, just include some CSS after the ``{% chat %}`` element,
e.g.:

.. code-block:: html+django

    {% chat %}

    <style>
        .otreechat .messages {
            height: 400px;
        }
        .otreechat .nickname {
            color: #0000FF;
            font-weight: bold;
        }
    </style>

Multiple chats on a page
~~~~~~~~~~~~~~~~~~~~~~~~

You can have multiple ``{% chat %}`` boxes on each page,
so that a player can be in multiple channels simultaneously.

For example, this code enables 1:1 chat with every other player in the group.

.. code-block:: python

    class Player(BasePlayer):

        def chat_nickname(self):
            return 'Player {}'.format(self.id_in_group)

        def chats(self):
            channels = []
            for other in self.get_others_in_group():
                if other.id_in_group < self.id_in_group:
                    lower_id, higher_id = other.id_in_group, self.id_in_group
                else:
                    lower_id, higher_id = self.id_in_group, other.id_in_group
                channels.append({
                    # make a name for the channel that is the same for all
                    # channel members. That's why we order it (lower, higher)
                    'channel': '{}-{}-{}'.format(self.group.id, lower_id, higher_id),
                    'label': 'Chat with {}'.format(other.chat_nickname())
                })
            return channels

.. code-block:: html+django

    {% for chat in player.chats %}
        <h4>{{ chat.label }}</h4>
        {% chat nickname=player.chat_nickname channel=chat.channel %}
    {% endfor %}


Exporting chat logs
~~~~~~~~~~~~~~~~~~~

Not yet implemented, coming soon