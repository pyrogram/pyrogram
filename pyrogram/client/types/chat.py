class Chat:
    def __init__(self,
                 id: int,
                 type: str,
                 title: str = None,
                 username: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 all_members_are_administrators: bool = None,
                 photo=None,
                 description: str = None,
                 invite_link: str = None,
                 pinned_message=None,
                 sticker_set_name: str = None,
                 can_set_sticker_set=None):
        ...
