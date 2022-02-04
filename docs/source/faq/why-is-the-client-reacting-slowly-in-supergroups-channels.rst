Why is the client reacting slowly in supergroups/channels?
==========================================================

Because of how Telegram works internally, every message you receive and send must pass through the creator's DC, and in
the worst case where you, the creator and another member all belong to three different DCs, the other member messages
have to go through from their DC to the creator's DC and finally to your DC. This is applied to each message and member
of a supergroup/channel and the process will inevitably take its time.

Another reason that makes responses come slowly is that messages are dispatched by priority. Depending on the kind
of member, some users receive messages faster than others and for big and busy supergroups the delay might become
noticeable, especially if you are among the lower end of the priority list:

1. Creator.
2. Administrators.
3. Bots.
4. Mentioned users.
5. Recent online users.
6. Everyone else.