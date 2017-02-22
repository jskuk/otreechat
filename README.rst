oTree Chat (beta)
=================

Chat rooms for oTree so that participants can communicate with each other.

This is an early beta version and subject to changes/improvements!

Installation
------------

(Assuming you already have an oTree project.)

Upgrade oTree-core (version 1.2 or higher required):

.. code-block::
    pip3 install -U otree-core

Install otreechat:

.. code-block::

    pip3 install -U otreechat

In ``settings.py``, add ``'otreechat'`` to ``INSTALLED_APPS``,
e.g. ``INSTALLED_APPS = ['otree', 'otreechat']``

Then run ``otree resetdb``.

(Also remember to put ``otreechat`` in your ``requirements_base.txt``,
so it gets installed on the server, etc.)

Usage
-----

Basic usage
~~~~~~~~~~~

Add ``{% load otreechat %}`` to the top of your template, e.g.:

.. code-block:: html+django

    {% load staticfiles otree_tags %}
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

Nickname
''''''''

``nickname`` is the nickname that will be displayed for that user in the chat.
A typical usage would be ``{% chat nickname=player.role %}``.

Channel
'''''''

``channel`` is the chat room's ID, meaning that if 2 players
have the same ``channel``, they can chat with each other.
``channel`` is not displayed in the user interface; it's just used internally.
Its default value is ``group.id``, meaning all players in the group can chat together.
You can use ``channel`` to instead scope the chat to the current page
or sub-division of a group, etc. (see examples below).
Regardless of the value of the ``channel`` argument,
the chat will at least be scoped to players in the same session and the same app.

Example: chat by role
`````````````````````

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

        def channel_nickname(self):
            return 'Group {} {}'.format(self.group.id_in_subsession, self.role())

Then in the template:

.. code-block:: html+django

    {% chat nickname=player.channel_nickname channel=player.role %}

Example: chat across rounds
```````````````````````````

If you need players to chat with players who are currently in a different round
of the game, you can do:

.. code-block:: html+django

    {% chat channel=group.id_in_subsession %}

Example: chat between all groups in all rounds
``````````````````````````````````````````````

If you want everyone in the session to freely chat with each other, just do:

.. code-block:: html+django

    {% chat channel=1 %}

(The number 1 is not significant; all that matters is that it's the same for everyone.)

Styling
~~~~~~~

To customize the style, just include some CSS after the ``{% chat %}`` element,
e.g.:

.. code-block:: html+django

    {% chat %}

    <style>
        .otree-chat .messages {
            height: 400px;
        }
        .otree-chat .nickname {
            color: #0000FF;
            font-weight: bold;
        }
    </style>

You can also customize the appearance by putting it inside a ``<div>``
and styling that parent ``<div>``. For example, to set the width:

.. code-block:: html+django

    <div style="width: 400px">
        {% chat nickname=player.chat_nickname channel=chat.channel %}
    </div>

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


Exporting CSV of chat logs
--------------------------

The chat logs download link will appear on oTree's regular data export page.

Upgrading
---------

During Februrary/March 2017, this package will be upgraded frequently
(e.g. to fix performance issues),
so you should upgrade frequently as well:

.. code-block::

    pip install -U otreechat

Feedback
--------

Please send any feedback/opinions to chris@otree.org,
for example to suggest an improvement to the widget's appearance.
