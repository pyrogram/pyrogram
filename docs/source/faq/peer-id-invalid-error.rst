PEER_ID_INVALID error
=====================

This error could mean several things:

- The chat id you tried to use is simply wrong, check it again.
- The chat id refers to a group or channel you are not a member of.
- The chat id argument you passed is in form of a string; you have to convert it into an integer with ``int(chat_id)``.
- The chat id refers to a user or chat your current session hasn't met yet.

About the last point: in order for you to meet a user and thus communicate with them, you should ask yourself how to
contact people using official apps. The answer is the same for Pyrogram too and involves normal usages such as searching
for usernames, meeting them in a common group, having their phone contacts saved, getting a message mentioning them
or obtaining the dialogs list.