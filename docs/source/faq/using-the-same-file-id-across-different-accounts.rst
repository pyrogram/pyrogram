Using the same file_id across different accounts
================================================

Telegram file_id strings are bound to the account which generated them. An attempt in using a foreign file id will
result in errors such as ``[400 MEDIA_EMPTY]``. The only exception are stickers' file ids; you can use them across
different accounts without any problem.