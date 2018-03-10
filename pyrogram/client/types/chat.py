class Chat:
    def __init__(self,
                 id: int,
                 type: str,
                 title: str = None,
                 username: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 all_members_are_administrators: bool = None,
                 photo: "ChatPhoto" = None,
                 description: str = None,
                 invite_link: str = None,
                 pinned_message: "Message" = None,
                 sticker_set_name: str = None,
                 can_set_sticker_set: bool = None):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.all_members_are_administrators = all_members_are_administrators
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
