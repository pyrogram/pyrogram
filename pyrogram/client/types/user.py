class User:
    """This object represents a Telegram user or bot.

    Args:
        id (:obj:`int`):
            Unique identifier for this user or bot.

        is_bot (:obj:`bool`):
            True, if this user is a bot.

        first_name (:obj:`str`):
            User's or bot’s first name.

        last_name (:obj:`str`, optional):
            User's or bot’s last name.

        username (:obj:`str`, optional):
            User's or bot’s username.

        language_code (:obj:`str`, optional):
            IETF language tag of the user's language.
    """

    def __init__(self,
                 id: int,
                 is_bot: bool,
                 first_name: str,
                 last_name: str = None,
                 username: str = None,
                 language_code: str = None):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
